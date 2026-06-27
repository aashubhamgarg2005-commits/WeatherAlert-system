from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.app.repository.user_repository import get_user_by_email
from backend.app.core.security import verify_password,create_access_token
import bcrypt
from backend.app.Schema.user import User, UserPreference, UserProfile


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def get_user_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, hashed_password: str) -> User:
    user = User(email=email, hash_password=hashed_password)
    db.add(user)
    db.flush()
    return user


def user_profile_create(db: Session, user_id: int, user_name: str, phone: str) -> UserProfile:
    profile = UserProfile(user_id=user_id, user_name=user_name, phone=phone)
    db.add(profile)
    return profile


def user_preference(
        db: Session,
        user_id: int,
        city_name: str,
        state_name: str
) -> UserPreference:
    preference = UserPreference(
        user_id=user_id,
        city_name=city_name,
        state_name=state_name
    )
    db.add(preference)
    return preference

def register_user(
        db:Session,
        email:str,
        password:str,
        user_name:str,
        phone:str,
        city_name:str,
        state_name:str
):
    try:
        existing_user = get_user_email(db,email)
        if existing_user :
            raise ValueError("Email Already Registered")

        hashed_password = hash_password(password)
        user = create_user(db=db,
                           email=email,
                           hashed_password=hashed_password)

        user_profile_create(db=db,
                            user_id=user.id,
                            user_name=user_name,
                            phone=phone)
        db.flush()

        user_preference(db=db,
                        user_id=user.id,
                        city_name=city_name,
                        state_name=state_name)

        db.commit()
        db.refresh(user)
        return user
    except ValueError:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise

def user_login(db:Session,
               email:str,
               password:str):
    user = get_user_by_email(db=db,
                             email=email)
    if not user:
        raise ValueError("Invalid Email")
    if not verify_password(password,user.hash_password):
        raise ValueError("Invalid Password")
    access_token = create_access_token(
        data={
            "sub":user.email,
            "user_id":user.id
        }
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
    
