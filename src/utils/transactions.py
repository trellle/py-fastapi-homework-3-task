from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession


def transaction_atomic(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db: AsyncSession = kwargs.get("db")
        if not db:
            raise ValueError("AsyncSession 'db' must be passed as a keyword argument.")
        async with db.begin():
            result = await func(*args, **kwargs)
        return result
    return wrapper
