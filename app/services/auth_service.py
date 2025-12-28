from app.repositories.user_repo import load_users


def login():
    users = load_users()

    print("\n🔐 INICIO DE SESIÓN")

    username = input("Usuario: ")
    password = input("Contraseña: ")

    for user in users:
        if user.username == username and user.password == password:
            print(f"\n✅ Bienvenido {user.username} ({user.role.upper()})")
            return user

    print("\n❌ Credenciales incorrectas")
    return None
