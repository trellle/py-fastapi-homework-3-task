from sqlalchemy.ext.asyncio import AsyncSession
from src.database import UserModel, UserGroupEnum, ActivationTokenModel
from src.schemas import UserRegistrationRequestSchema
from src.security.passwords import hash_password
from src.utils.transactions import transaction_atomic
from src.exceptions import UserCreateException
from datetime import datetime, timezone, timedelta
import secrets


@transaction_atomic
async def create_user(db: AsyncSession, user: UserRegistrationRequestSchema):
    try:
        hashed = hash_password(user.password)
        db_user = UserModel(email=user.email,
                            _hashed_password=hashed,
                            group=UserGroupEnum.USER)
        token = ActivationTokenModel(user_id=db_user.id,
                                    token=secrets.token_urlsafe(32),
                                    expires_at=(datetime.now(timezone.utc) + timedelta(hours=1)))
        db.add_all([db_user, token])
        await db.flush()
        await db.refresh(db_user)
        return db_user
    except Exception:
        raise UserCreateException()
