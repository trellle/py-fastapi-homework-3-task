from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from src.exceptions import UserCreateException, PasswordResetException
from fastapi import HTTPException, status


def transaction_atomic(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db: AsyncSession = kwargs.get("db")
        if not db:
            raise ValueError("AsyncSession 'db' must be passed as a keyword argument.")
        try:
            async with db.begin():
                result = await func(*args, **kwargs)
                return result
        except UserCreateException:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during user creation.")
        except PasswordResetException:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while resetting the password.")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred")
    return wrapper
