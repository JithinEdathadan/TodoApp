from fastapi import APIRouter, Depends
from TodoApp.Database import Database
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from TodoApp.services.UserServices import UserServices
from TodoApp.schemas.UserUpdateSchema import UserUpdateSchema

from TodoApp.services.AuthServices import AuthServices

router = APIRouter(
    prefix="/user",
    tags=['User']
)

db_object = Database()
db_dependency = Annotated[Session,Depends(db_object.get_db)]

auth_services_obj = AuthServices()
user_dependency = Annotated[dict,Depends(auth_services_obj.get_current_user)] # get_current_user is expected to return and dict

auth_services_obj = AuthServices()
admin_dependency = Annotated[bool,Depends(auth_services_obj.is_current_user_admin)]

user_services = UserServices()

@router.get("/",status_code=status.HTTP_200_OK)
async def get_user_by_id(user:user_dependency,db:db_dependency):
    return user_services.get_user_by_id(db,user.get('id'))

@router.put("/",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency,db:db_dependency,user_request_data:UserUpdateSchema,is_admin:admin_dependency):
    return user_services.update_user(db,user_request_data,user.get('id'),is_admin)