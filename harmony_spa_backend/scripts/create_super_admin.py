from getpass import getpass
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.core.security import hash_password
from app.domain.enums.user_role import UserRole
from app.infrastructure.database.session import SessionLocal
from app.models import User

def main():
    db = SessionLocal()
    try:
        existing = db.scalar(select(User).where(User.role == UserRole.SUPER_ADMIN))
        if existing:
            print("Ya existe un SUPER_ADMIN. No se creará otro."); return
        print("\n=== CREACIÓN DEL SUPER_ADMIN ===")
        first = input("Nombres: ").strip(); last = input("Apellidos: ").strip(); email = input("Correo electrónico: ").strip().lower()
        password = getpass("Contraseña (mínimo 12 caracteres): "); confirm = getpass("Confirma la contraseña: ")
        if not first or not last or "@" not in email: raise ValueError("Debes ingresar nombres, apellidos y correo válido.")
        if password != confirm: raise ValueError("Las contraseñas no coinciden.")
        user = User(first_name=first, last_name=last, email=email, password_hash=hash_password(password), role=UserRole.SUPER_ADMIN, is_active=True)
        db.add(user); db.commit()
        print("SUPER_ADMIN creado correctamente.")
    except IntegrityError:
        db.rollback(); print("No se pudo crear: el correo o el SUPER_ADMIN ya existe.")
    finally: db.close()
if __name__ == "__main__": main()
