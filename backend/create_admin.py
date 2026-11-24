from getpass import getpass

from backend.services.auth_service import ServicioAutenticacion


def main() -> None:
    service = ServicioAutenticacion()
    username = input("Usuario administrador: ")
    password = getpass("Contraseña (mínimo 12 caracteres): ")
    confirmation = getpass("Repite la contraseña: ")
    if password != confirmation:
        raise SystemExit("Las contraseñas no coinciden.")
    try:
        user = service.crear_usuario(username, password, "admin")
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print(f"Administrador '{user['username']}' creado.")


if __name__ == "__main__":
    main()
