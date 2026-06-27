from sqlalchemy.orm import Session
from backend.app.Schema.user import User, UserPreference, UserProfile


def get_user_email(db:Session,email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,
                email:str,
                hashed_password:str):
    new_user = User(
        email = email,
        hash_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def user_profile_create(db:Session,
                       user_id:int,
                        user_name:str,
                         phone:str | None = None):
    profile = UserProfile(
        user_id = user_id,
        user_name = user_name,
        phone = phone
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def user_preference(db:Session,
                 user_id : int,
                    city_name:str,
                    state_name:str,
                    latitude=None,
                    longitude=None,
                    device_token=None,
                    notify_via_push=True,
                    alert_level="severe"  ):
    preference=UserPreference(
        user_id = user_id,
        city_name = city_name,
        state_name = state_name,
        latitude = latitude,
        longitude = longitude,
        device_token = device_token,
        notify_via_push = notify_via_push,
        alert_level = alert_level)

    db.add(preference),
    db.commit(),
    db.refresh(preference)

    return preference


def get_user_detail_id(db:Session,
                       user_id:int):

    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db:Session,
                      email:str):
    return db.query(User).filter(User.email == email).first()

    
