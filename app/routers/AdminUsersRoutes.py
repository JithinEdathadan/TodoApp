from fastapi import APIRouter, Depends, HTTPException
from app.Database import Database
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from app.services.UserServices import UserServices
from app.schemas.UserUpdateSchema import UserUpdateSchema

from app.services.AuthServices import AuthServices

router = APIRouter(
    prefix="/admin/user",
    tags=['Admin']
)

db_object = Database()
db_dependency = Annotated[Session,Depends(db_object.get_db)]

auth_services_obj = AuthServices()
user_dependency = Annotated[dict,Depends(auth_services_obj.get_current_user)] # get_current_user is expected to return and dict

auth_services_obj = AuthServices()
admin_dependency = Annotated[bool,Depends(auth_services_obj.is_current_user_admin)]

user_services = UserServices()

@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_users(is_admin:admin_dependency,db:db_dependency):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorisation failed')
    return user_services.get_all_users(db)

@router.put("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db:db_dependency,user_request_data:UserUpdateSchema,is_admin:admin_dependency,user_id:int):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorisation failed')
    return user_services.update_user(db,user_request_data,user_id,is_admin)