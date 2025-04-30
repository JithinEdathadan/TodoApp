from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email:Optional[EmailStr] = None
    first_name:Optional[str] = None
    last_name:Optional[str] = None
    role:Optional[str] = None