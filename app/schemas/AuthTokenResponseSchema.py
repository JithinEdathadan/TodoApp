from pydantic import BaseModel
class AuthTokenResponseSchema(BaseModel):
    access_token:str
    token_type:str