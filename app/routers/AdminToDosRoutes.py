from fastapi import APIRouter, HTTPException, Depends, Path
from app.Database import Database
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from starlette import status
from app.services.AuthServices import AuthServices
from app.services.ToDosServices import ToDosServices
from app.schemas.ToDosSchema import ToDosSchema
from app.services.UserServices import UserServices

router = APIRouter(
    prefix="/admin/to-dos",
    tags=['Admin']
)

db_object = Database()
db_dependency = Annotated[Session,Depends(db_object.get_db)]

auth_services_obj = AuthServices()
admin_dependency = Annotated[bool,Depends(auth_services_obj.is_current_user_admin)]

user_dependency = Annotated[dict,Depends(auth_services_obj.get_current_user)] # get_current_user is expected to return and dict
to_dos_services = ToDosServices()

@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_to_dos(is_admin:admin_dependency,db:db_dependency,user_id : Optional[int] = None):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorisation failed')
    if user_id is None:
        user_id = 0
    return to_dos_services.get_all_to_dos(db,user_id,is_admin)

@router.get("/{to_id}",status_code=status.HTTP_200_OK)
async def get_to_do_by_id(is_admin:admin_dependency,db:db_dependency,to_id:int = Path(gt=0)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorisation failed')
    return to_dos_services.get_to_do_by_id(db,to_id,0,is_admin)

@router.post("/add",status_code=status.HTTP_201_CREATED)
async def add_to_do(user:user_dependency,is_admin:admin_dependency,db:db_dependency,new_to_do:ToDosSchema,user_id : Optional[int] = None):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorisation failed')
    if user_id is None:
        # if user_id is passed as params then add to the specific user if not add to the admin To-Do's list
        user_id = user.get('id')
    else:
        # verify the user with given id exist
        try:
            UserServices().get_user_by_id(user_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Unable to load user: {user_id}')
    return to_dos_services.add_to_do(db, new_to_do, user_id)

@router.put("/{to_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(is_admin:admin_dependency,db:db_dependency,to_do_request:ToDosSchema,to_id:int = Path(gt=0)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authorisation failed')
    return to_dos_services.update_todo(db,to_do_request,to_id,0,is_admin)

@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(is_admin:admin_dependency,db:db_dependency,todo_id:int = Path(gt=0)):
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorisation failed')
    return to_dos_services.delete_by_id(db,todo_id,0,is_admin)