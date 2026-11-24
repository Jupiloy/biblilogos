import hashlib
import hmac
import secrets
import sqlite3
import time
from pathlib import Path


ITERACIONES_HASH = 600_000
DURACION_SESION = 8 * 60 * 60
ROLES_VALIDOS = {"admin", "lector"}


class UsuarioDuplicadoError(ValueError):
    """Se intenta registrar un nombre de usuario ya existente."""


class ServicioAutenticacion:
    def __init__(self, database_path: str | Path | None = None) -> None:
        self.database_path = (
            Path(database_path)
            if database_path is not None
            else Path(__file__).resolve().parents[2] / "data" / "usuarios.db"
        )
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_salt TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('admin', 'lector')),
                    created_at INTEGER NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    expires_at INTEGER NOT NULL
                )
                """
            )

    @staticmethod
    def normalizar_usuario(username: str) -> str:
        normalized = username.strip().lower()
        if not 3 <= len(normalized) <= 32:
            raise ValueError("El usuario debe tener entre 3 y 32 caracteres.")
        if not all(char.isalnum() or char in "._-" for char in normalized):
            raise ValueError(
                "El usuario solo puede contener letras, números, punto, guion y guion bajo."
            )
        return normalized

    @staticmethod
    def _validar_contrasena(password: str) -> None:
        if len(password) < 12:
            raise ValueError("La contraseña debe tener al menos 12 caracteres.")
        if len(password) > 128:
            raise ValueError("La contraseña no puede superar 128 caracteres.")

    @staticmethod
    def _hash_contrasena(password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, ITERACIONES_HASH
        )

    def crear_usuario(self, username: str, password: str, role: str) -> dict:
        normalized = self.normalizar_usuario(username)
        self._validar_contrasena(password)
        if role not in ROLES_VALIDOS:
            raise ValueError("El rol debe ser 'admin' o 'lector'.")

        salt = secrets.token_bytes(16)
        password_hash = self._hash_contrasena(password, salt)
        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO users (
                        username, password_salt, password_hash, role, created_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        normalized,
                        salt.hex(),
                        password_hash.hex(),
                        role,
                        int(time.time()),
                    ),
                )
                user_id = cursor.lastrowid
        except sqlite3.IntegrityError as error:
            raise UsuarioDuplicadoError(
                "Ese nombre de usuario ya está registrado."
            ) from error

        return {"id": user_id, "username": normalized, "role": role}

    def iniciar_sesion(self, username: str, password: str) -> dict | None:
        normalized = username.strip().lower()
        with self._connect() as connection:
            user = connection.execute(
                """
                SELECT id, username, password_salt, password_hash, role
                FROM users WHERE username = ?
                """,
                (normalized,),
            ).fetchone()

        if user is None:
            return None

        salt = bytes.fromhex(user["password_salt"])
        expected = bytes.fromhex(user["password_hash"])
        actual = self._hash_contrasena(password, salt)
        if not hmac.compare_digest(actual, expected):
            return None

        token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + DURACION_SESION
        token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
        with self._connect() as connection:
            connection.execute("DELETE FROM sessions WHERE expires_at <= ?", (int(time.time()),))
            connection.execute(
                "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
                (token_hash, user["id"], expires_at),
            )
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": DURACION_SESION,
            "username": user["username"],
            "role": user["role"],
        }

    def autenticar_token(self, token: str) -> dict | None:
        try:
            token_bytes = token.encode("ascii")
        except UnicodeEncodeError:
            return None
        token_hash = hashlib.sha256(token_bytes).hexdigest()
        now = int(time.time())
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT users.id, users.username, users.role
                FROM sessions
                JOIN users ON users.id = sessions.user_id
                WHERE sessions.token_hash = ? AND sessions.expires_at > ?
                """,
                (token_hash, now),
            ).fetchone()
            connection.execute("DELETE FROM sessions WHERE expires_at <= ?", (now,))
        if row is None:
            return None
        return {"id": row["id"], "username": row["username"], "role": row["role"]}

    def cerrar_sesion(self, token: str) -> None:
        token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
        with self._connect() as connection:
            connection.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
