from pydantic import BaseModel, EmailStr, field_validator, ConfigDict

from src.database import accounts_validators
from src.database.models.accounts import UserGroupEnum


class UserBase(BaseModel):
    email: EmailStr


class UserRegistrationRequestSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)

    password: str

    @field_validator("email")
    def validate_email(cls, value: EmailStr):
        accounts_validators.validate_email(value)

    @field_validator("password")
    def validate_password_reliability(cls, value: str):
        accounts_validators.validate_password_strength(value)


class UserRegistrationResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserActivationRequestSchema(UserBase):
    token: str
