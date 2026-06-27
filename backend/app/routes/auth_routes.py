from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from backend.app.core.database_connection import get_db
from backend.app.Schema.user_schema import UserCreate,userLogin
from backend.app.core.auth import current_user

# Import the whole module to prevent Circular Import issues
from backend.app.services import auth_services

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.get("/profile")
def get_profile(
    current_user = Depends(current_user),
    db: Session = Depends(get_db)
):
    from backend.app.Schema.user import UserPreference
    preference = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    return {
        "id": current_user.id,
        "email": current_user.email,
        "city": preference.city_name if preference else None,
        "state": preference.state_name if preference else None,
        "user_name": current_user.profile.user_name if current_user.profile else None
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Call the service function with all 7 required arguments from UserCreate schema
        new_user = auth_services.register_user(
            db=db,
            email=user.email,
            password=user.password,
            user_name=user.user_name, 
            phone=user.phone,
            city_name=user.city_name,
            state_name=user.state     # Maps 'state' from schema to 'state_name' in service
        )
        return {
            "message": "User Registered Successfully",
            "user_id": new_user.id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error while registering user"
        )

@router.post("/login")
def login(
    user:userLogin,
    db:Session = Depends(get_db)
):
    try:
        token = auth_services.user_login(db=db,
                                         email=user.email,
                                         password=user.password)
        return token

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail= str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database Error while login"
        )

@router.get("/me")
def get_me(
    current_user = Depends(current_user)
):
    return {
        "id":current_user.id,
        "email":current_user.email,
        "is_active":current_user.is_active
    }


@router.get("/protected")
def protected_route(
    current_user = Depends(current_user)
):
    return{
        "message":"Access Granted",
        "user":current_user.email
    }

@router.get("/preferences")
def get_preferences(
    current_user=Depends(current_user),
    db: Session = Depends(get_db)
):
    from backend.app.Schema.user import UserPreference
    pref = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    return {
        "notify_via_push": pref.notify_via_push if pref else True,
        "alert_level": pref.alert_level if pref else "severe"
    }

@router.put("/preferences")
def update_preferences(
    data: dict,
    current_user=Depends(current_user),
    db: Session = Depends(get_db)
):
    from backend.app.Schema.user import UserPreference
    pref = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()
    if pref:
        if "notify_via_push" in data:
            pref.notify_via_push = data["notify_via_push"]
        if "alert_level" in data:
            pref.alert_level = data["alert_level"]
        db.commit()
    return {"message": "Preferences updated successfully"}