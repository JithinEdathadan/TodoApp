from fastapi import APIRouter, Depends

from app.schemas.UserSchema import UserSchema
from app.Database import Database
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from app.services.AuthServices import AuthServices
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.AuthTokenResponseSchema import AuthTokenResponseSchema
from app.schemas.AuthChangePasswordSchema import AuthChangePasswordSchema

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

db_object = Database()
db_dependency = Annotated[Session,Depends(db_object.get_db)]
auth_services = AuthServices()

admin_dependency = Annotated[bool,Depends(auth_services.is_current_user_admin)]
user_dependency = Annotated[dict,Depends(auth_services.get_current_user)]

@router.post("/create-user",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,user_data:UserSchema,is_admin:admin_dependency):
    return auth_services.create_user(db,user_data,is_admin)
@router.post("/token",status_code=status.HTTP_200_OK, response_model=AuthTokenResponseSchema)
async def login_with_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    return auth_services.authenticate_user(db, form_data)
@router.put("/change-password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db:db_dependency,user:user_dependency,passwords:AuthChangePasswordSchema):
    return auth_services.reset_password(db,passwords,user.get('id'))


# JWT: head body secret