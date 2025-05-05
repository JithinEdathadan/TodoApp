from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    username:str = Field(min_length=3)
    email:EmailStr
    first_name:str
    last_name:str
    password:str
    role:Optional[str] = Field(description="Default role is user", default="user")
    phone_number:str