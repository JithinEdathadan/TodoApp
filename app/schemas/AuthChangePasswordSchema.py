from pydantic import BaseModel

class AuthChangePasswordSchema(BaseModel):
    password:str
    new_password:str