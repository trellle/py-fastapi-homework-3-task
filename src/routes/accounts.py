from datetime import datetime, timezone
from typing import cast

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from src.config import get_jwt_auth_manager, get_settings, BaseAppSettings
from src.database import (
    get_db,
    UserModel,
    UserGroupModel,
    UserGroupEnum,
    ActivationTokenModel,
    PasswordResetTokenModel,
    RefreshTokenModel
)
from exceptions import BaseSecurityError
from src.security.interfaces import JWTAuthManagerInterface
from src.schemas import (
    UserRegistrationRequestSchema,
    UserRegistrationResponseSchema,
    UserActivationRequestSchema
)
from src.crud.users import create_user

router = APIRouter()


@router.post("/register/", response_model=UserRegistrationResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegistrationRequestSchema,
                   db: AsyncSession = Depends(get_db)) -> UserRegistrationResponseSchema:
    try:
        result = await db.execute(select(UserModel).where(UserModel.email == user.email))
        db_user = result.scalar_one_or_none()
        if db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A user with this email {user.email} already exists.")
        return await create_user(db, user)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during user creation.")


@router.post("/activate/", response_model=UserActivationRequestSchema)
async def activate_user(db: AsyncSession = Depends(get_db)):
    result = db.execute(select(ActivationTokenModel))
