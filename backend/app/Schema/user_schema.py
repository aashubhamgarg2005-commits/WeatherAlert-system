from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

class UserCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_name:str = Field(validation_alias=AliasChoices("user_name", "username", "userName"))
    email:str
    phone:str
    password:str
    city_name:str = Field(validation_alias=AliasChoices("city_name", "cityName", "city"))
    state:str = Field(validation_alias=AliasChoices("state", "state_name", "stateName"))

    @field_validator("user_name", "phone", "city_name", "state", mode="before")
    @classmethod
    def convert_to_string(cls, value):
        return str(value).strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.rsplit("@", 1)[-1]:
            raise ValueError("Invalid email address")
        return value

class userLogin(BaseModel):
    email:str
    password:str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or "." not in value.rsplit("@", 1)[-1]:
            raise ValueError("Invalid email address")
        return value

class UserResponse(BaseModel):
    id :int
    email:str
    
model_config = {"from_attributes": True}
