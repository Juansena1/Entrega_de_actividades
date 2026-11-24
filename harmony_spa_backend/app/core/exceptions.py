from fastapi import HTTPException, status

def credentials_exception() -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas o sesión no válida", headers={"WWW-Authenticate": "Bearer"})
