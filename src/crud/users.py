from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import UserModel, UserGroupEnum
from src.schemas import UserRegistrationRequestSchema
from src.security.passwords import hash_password
from src.utils.transactions import transaction_atomic
from src.security.token_manager import JWTAuthManager


@transaction_atomic
async def create_user(db: AsyncSession, user: UserRegistrationRequestSchema):
    hashed = hash_password(user.password)
    token = JWTAuthManager._create_token()
    db_user = UserModel(email=user.email,
                        _hashed_password=hashed,
                        group=UserGroupEnum.USER,
                        activation_token=token)
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    return db_user
