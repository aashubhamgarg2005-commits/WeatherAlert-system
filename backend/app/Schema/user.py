from sqlalchemy import Integer,Column,String,Boolean,ForeignKey,DateTime,Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.core.database_connection import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    email = Column(String,unique=True,index=True,nullable=False)
    hash_password = Column(String,nullable=False)
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default=False)
    profile = relationship("UserProfile",back_populates="user",uselist=False,cascade="all, delete-orphan")
    preference = relationship("UserPreference",back_populates="user",cascade="all,delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),unique=True)
    user_name = Column(String,nullable=False)
    phone = Column(String(15),unique=True,nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
    user = relationship("User",back_populates="profile")

class UserPreference(Base):
    __tablename__ = "user_preference"
    id = Column(Integer,primary_key=True,index=True)
    user_id =Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    city_name = Column(String,nullable=False)
    state_name = Column(String,nullable=False)
    latitude = Column(Numeric(9,6),nullable=True)
    longitude = Column(Numeric(9,6),nullable=True)
    device_token = Column(String,nullable=True)
    notify_via_push = Column(Boolean,default=True)
    alert_level = Column(String(20),default="severe")
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    user = relationship("User",back_populates="preference")


users = User
