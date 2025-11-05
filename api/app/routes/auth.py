from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from datetime import datetime, timezone

# core
# session
from app.core.session import get_db
# security
from app.core.security import create_password_hash, verify_password_hash, generate_access_token, verify_token

# models
from app.models.user_model import User
# schemas
from app.models.schemas.user_schema import UserCreate, UserLogin, UserOut, Token

# services
from app.services import user_service

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

router = APIRouter(prefix="/auth", tags=["auth"])

# register the user 
@router.post("/register", response_model=UserOut, name="registerUser")
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    if user_service.email_finder(payload.email, db):
        THROW_ERROR("Email already in use.", 400)

    _password = create_password_hash(payload.password)

    user = User(
        email = payload.email,
        password_hash = _password,
        # default = staff
        # role = "staff" ->  "admin" ( [uncomment] here change if u want to create an admin || create a function to create admins )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# login the user
@router.post("/login", response_model=Token, name="loginUser")
def login_user(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    if not user_service.email_finder(payload.email,db):
        THROW_ERROR("Accont was not found!", 400)
    
    user = user_service.email_finder(payload.email,db)

    if not verify_password_hash(payload.password, user.password_hash):
        THROW_ERROR("Incorrect password!", 401)

    access_token = generate_access_token(
        subject= str(user.id),
        minutes= 15,
    )

    refresh_token = generate_access_token(
        subject= str(user.id),
        minutes=60*24*30,
        scope="refresh",
    )

    user.last_login = datetime.now(timezone.utc)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# refresh JWT token
@router.post("/refresh", response_model=Token, name="refreshToken")
def refresh_token(payload: dict = Body(...)):
    token = payload.get("refresh_token")
    if not token:
        THROW_ERROR("Refresh token required", 400)

    claims = verify_token(token)
    if claims.get("scope") != "refresh":
        THROW_ERROR("Invalid refresh token", 403)

    new_access_token = generate_access_token(
        subject=claims["sub"],
        minutes=15
    )

    return {
        "access_token": new_access_token,
        "refresh_token": token, 
        "token_type": "bearer"
    }
