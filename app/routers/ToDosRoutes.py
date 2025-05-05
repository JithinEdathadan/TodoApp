from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette import status

from app.Database import Database
from app.schemas.ToDosSchema import ToDosSchema
from app.services.ToDosServices import ToDosServices

from app.services.AuthServices import AuthServices

router = APIRouter(
    prefix="/todo",
    tags=['To-Do']
)
db_object = Database()
db_dependency = Annotated[Session,Depends(db_object.get_db)]

auth_services_obj = AuthServices()
user_dependency = Annotated[dict,Depends(auth_services_obj.get_current_user)] # get_current_user is expected to return and dict
to_dos_services = ToDosServices()

@router.get("/",status_code=status.HTTP_200_OK)
async def get_all_to_dos(user:user_dependency,db:db_dependency):
    return to_dos_services.get_all_to_dos(db,user.get('id'))

@router.get("/{to_id}",status_code=status.HTTP_200_OK)
async def get_to_do_by_id(user:user_dependency,db:db_dependency, to_id:int = Path(gt=0)):
    return to_dos_services.get_to_do_by_id(db,to_id,user.get('id'))

@router.post("/add",status_code=status.HTTP_201_CREATED)
async def add_to_do(user:user_dependency,db:db_dependency,new_to_do:ToDosSchema):
    return to_dos_services.add_to_do(db, new_to_do,user.get('id'))

@router.put("/{to_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency,db:db_dependency,to_do_request:ToDosSchema,to_id:int = Path(gt=0)):
    return to_dos_services.update_todo(db,to_do_request,to_id,user.get('id'))

@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(user:user_dependency,db:db_dependency,todo_id:int = Path(gt=0)):
    return to_dos_services.delete_by_id(db,todo_id,user.get('id'))
