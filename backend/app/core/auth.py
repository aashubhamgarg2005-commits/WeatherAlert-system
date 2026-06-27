from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from config import Config
from backend.app.core.connection import get_db
from backend.app.repository.user_repository import get_user_by_email

config = Config()  # Object banao

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def current_user(token: str = Depends(oauth2_schema),
                 db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not Validate credentials"
    )
    try:
        payload = jwt.decode(
            token, config.secret_key,
            algorithms=[config.algorithem]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user