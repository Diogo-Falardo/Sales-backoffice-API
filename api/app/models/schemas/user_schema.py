from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR
# helpers
from app.utils.helpers import user_helper


# ---- Base ----
class UserBase(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, email):
        return user_helper.validate_email(email)
    

# ---- Create ----
class UserCreate(UserBase):
    password: str 

    @field_validator("password")
    @classmethod
    def _password(cls, password):
        return user_helper.validate_password(password)
    
# ---- Update ----
class UserChangeEmail(BaseModel):
    email: EmailStr
    
    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, email):
        return user_helper.validate_email(email)

class UserChangePassword(BaseModel):
    password: str
    new_password: str

    @field_validator("password")
    @classmethod
    def _password(cls, password):
        return user_helper.validate_password(password)
    
    @field_validator("new_password")
    @classmethod
    def _new_password(cls, new_password):
        return user_helper.validate_password(new_password)

# ---- Read/Out ----
class UserOut(UserBase):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Login ----
class UserLogin(BaseModel):
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def _email(cls, email):
        return user_helper.validate_email(email)

    password: str 

    @field_validator("password")
    @classmethod
    def _password(cls, password):
        return user_helper.validate_password(password)

# --- JWT ----
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str