from pydantic import BaseModel

class AlertResponse(BaseModel):
    type:str
    message:str
