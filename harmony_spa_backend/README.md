# Harmony Spa Backend

Backend REST basado en los seis documentos de referencia. Incluye FastAPI, SQLAlchemy 2, MySQL, Alembic, Pydantic, JWT, Argon2, gestión de sesiones, siete modelos ORM y módulo de usuarios.

## Requisitos
- Python 3.11 o superior recomendado.
- MySQL 8 y una instancia local activa.
- Visual Studio Code.

## Instalación en Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edita `.env`: configura `DATABASE_URL` con tu usuario/contraseña MySQL y genera una clave JWT:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```
Copia el resultado en `JWT_SECRET_KEY`. No compartas `.env` ni lo subas a Git.

## Crear la base de datos
En MySQL Workbench ejecuta:
```sql
CREATE DATABASE harmony_spa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
La base debe existir antes de migrar. El usuario MySQL configurado necesita permisos sobre ella.

## Migraciones
```powershell
alembic revision --autogenerate -m "crear modelos iniciales harmony spa"
alembic upgrade head
```
La primera orden genera la revisión inicial y la segunda crea las tablas en MySQL. Revisa siempre el archivo generado en `migrations/versions/` antes de aplicar. En instalaciones posteriores, cuando ya exista una revisión, normalmente bastará con `alembic upgrade head`.
Revisa siempre el archivo generado en `migrations/versions/` antes de aplicar. No borres migraciones ya aplicadas.

## Crear SUPER_ADMIN inicial
```powershell
python -m scripts.create_super_admin
```
El script solicita nombres, correo y contraseña de forma interactiva. No existe endpoint público para crear SUPER_ADMIN.

## Ejecutar
```powershell
uvicorn app.main:app --reload
```
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Salud: http://127.0.0.1:8000/health
- MySQL: http://127.0.0.1:8000/health/ready

## Endpoints incluidos
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`
- `POST /api/v1/users` (SUPER_ADMIN)
- `GET /api/v1/users` (SUPER_ADMIN)
- `GET /api/v1/users/{user_id}` (SUPER_ADMIN)
- `PATCH /api/v1/users/{user_id}` (SUPER_ADMIN)
- `PATCH /api/v1/users/{user_id}/status` (SUPER_ADMIN)

Las respuestas públicas nunca incluyen `password_hash`. Se permiten sesiones simultáneas; cerrar sesión revoca solamente el token actual. Desactivar un usuario revoca todas sus sesiones activas.

## Modelos ORM
`users`, `user_sessions`, `client_profiles`, `employee_profiles`, `procedures`, `procedure_sessions`, `appointments`.
Los documentos delimitan aquí el ORM a esas siete tablas. Los tratamientos y sus sesiones reales quedan para una fase posterior.

## Pruebas
```powershell
python -m compileall app scripts
pytest
```
La prueba de salud básica no requiere conexión a MySQL. Para `health/ready`, MySQL debe estar disponible.
