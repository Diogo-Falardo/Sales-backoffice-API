from sqlalchemy.orm import Session


# models
from app.models.user_model import User

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

def get_user_from_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        THROW_ERROR("Invalid user", 400)
    
    return user


"""
finders
"""

def email_finder(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    
    return False

