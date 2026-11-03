# CRUD_SQLAlchemy

Aplicación CRUD de personas con Flask, Flask-SQLAlchemy, Flask-Migrate y MySQL.

## 1. Requisitos

- Python 3.10 o superior.
- MySQL Server iniciado.
- Visual Studio Code (recomendado).

## 2. Crear la base de datos

En MySQL Workbench ejecuta:

```sql
CREATE DATABASE flask_sqlalchemy
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

## 3. Configurar la conexión

Abre `app.py` y cambia:

```python
DB_PASSWORD = os.getenv("DB_PASSWORD", "TU_CONTRASEÑA")
```

Reemplaza `TU_CONTRASEÑA` por la contraseña real de tu usuario MySQL (por ejemplo, `root`). No escribas la palabra `root` si esa no es tu contraseña. Si tu MySQL usa otro puerto o usuario, ajusta `DB_HOST` o las variables de entorno correspondientes.

## 4. Crear y activar el entorno virtual (PowerShell)

Abre una terminal en la carpeta del proyecto y ejecuta:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, puedes ejecutar esta orden solo para la terminal actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 5. Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Crear las tablas con Flask-Migrate

Ejecuta los comandos desde la carpeta donde está `app.py`, con el entorno virtual activo:

```powershell
flask --app app db init
flask --app app db migrate -m "Migracion inicial MySQL"
flask --app app db upgrade
```

**Importante:** `flask db init` se ejecuta solamente la primera vez. Si ya existe la carpeta `migrations`, no lo repitas. Si `flask db migrate` indica que no detecta cambios, verifica la conexión y que la clase `Person` esté declarada en `app.py`.

## 7. Ejecutar la aplicación

```powershell
flask --app app --debug run
```

Abre en el navegador: http://127.0.0.1:5000

## 8. Crear requirements.txt nuevamente (opcional)

Si instalas otras librerías y quieres guardar las versiones exactas de tu entorno:

```powershell
pip freeze > requirements.txt
```

## Funcionalidades

- Listar personas.
- Crear personas.
- Editar personas.
- Eliminar personas.
- Validación básica de campos y correo único.

## Nota de seguridad

Este proyecto es de práctica y usa el servidor de desarrollo de Flask. No lo publiques en producción con `debug=True` ni con la clave secreta predeterminada.
