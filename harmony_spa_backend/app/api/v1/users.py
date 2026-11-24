from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.dependencies import require_super_admin
from app.domain.enums.user_role import UserRole
from app.infrastructure.database.session import get_db
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserStatusUpdate
from app.services.user_service import UserService
router = APIRouter()
@router.post("", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    return UserService.create_user(db, data)
@router.get("", response_model=list[UserResponse])
def list_users(role: UserRole | None = Query(default=None), is_active: bool | None = Query(default=None), skip: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100), db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    return UserRepository.list_users(db, role, is_active, skip, limit)
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    from fastapi import HTTPException
    user = UserRepository.get_by_id(db, user_id)
    if not user: raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    return UserService.update_user(db, user_id, data)
@router.patch("/{user_id}/status", response_model=UserResponse)
def change_user_status(user_id: int, data: UserStatusUpdate, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    return UserService.change_status(db, user_id, data.is_active)
