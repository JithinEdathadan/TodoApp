from fastapi import HTTPException, Depends
from TodoApp.models.ToDosModel import ToDosModel
from typing import Annotated
from TodoApp.Database import Database
from sqlalchemy.orm import Session
from TodoApp.schemas.ToDosSchema import ToDosSchema
from starlette import status

class ToDosServices:
    db_object = Database()
    db_dependency = Annotated[Session, Depends(db_object.get_db)]

    # get the To-DO's by user_id
    # for admin user pass the user_id as 0 and is_admin as true
    def get_all_to_dos(self,db,user_id:int,is_admin=False):
        if is_admin and user_id == 0:
            return db.query(ToDosModel).all()
        else:
            return db.query(ToDosModel).filter(ToDosModel.owner == user_id).all()

    # get the To-DO's by user_id and TO Do's ID
    # for admin user pass the user_id as 0 and is_admin as true
    def get_to_do_by_id(self,db:db_dependency,to_id:int,user_id:int,is_admin=False):
        if is_admin and user_id == 0:
            todo_model = db.query(ToDosModel).filter(ToDosModel.id == to_id).first()
        else:
            todo_model = db.query(ToDosModel).filter(ToDosModel.id == to_id).filter(ToDosModel.owner == user_id).first()
        if todo_model is not None:
            return todo_model
        raise HTTPException(status_code=404, detail=f'no ToDo\'s with ID : {to_id} for the current user')

    # add To-DO's to user account
    # admin can add To-DO's by passing any user id, for user the corresponding id is automatically taken into consideration
    def add_to_do(self,db:db_dependency,to_do_item:ToDosSchema,user_id:str):
        to_do_object = ToDosModel(**to_do_item.model_dump(),owner = user_id)
        try:
            db.add(to_do_object)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Exception occurred on data save: {repr(e)}')

    # update To-Do's by id and user ID
    # admin can update any user TO-Do's by passing is_admin = true and user_id =0
    def update_todo(self,db:db_dependency, to_do_request:ToDosSchema, to_id:int,user_id:int,is_admin =False):
        if is_admin and user_id == 0:
            todo_mode = db.query(ToDosModel).filter(ToDosModel.id == to_id).first()
        else:
            todo_mode = db.query(ToDosModel).filter(ToDosModel.id == to_id).filter(ToDosModel.owner == user_id).first()
        if todo_mode is None:
            raise HTTPException(status_code=404, detail=f'Unable to locate ToDo with ID {to_id}')
        todo_mode.title = to_do_request.title
        todo_mode.description = to_do_request.description
        todo_mode.priority = to_do_request.priority
        todo_mode.complete = to_do_request.complete
        try:
            db.add(todo_mode)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Exception occurred on data save: {repr(e)}')

    # Delete TO-Do's by id and user ID
    # Admin can delete any TO-Do's by passing the is_admin = True and user_id = 0
    def delete_by_id(self,db:db_dependency, todo_id:int,user_id:int,is_admin=False):
        if is_admin and user_id == 0:
            todo_model = db.query(ToDosModel).filter(ToDosModel.id == todo_id).first()
        else:
            todo_model = db.query(ToDosModel).filter(ToDosModel.id == todo_id).filter(ToDosModel.owner == user_id).first()
        if todo_model is None:
            raise HTTPException(status_code=404, detail=f'Unable to locate ToDo with ID {todo_id}')
        try:
            db.query(ToDosModel).filter(ToDosModel.id == todo_id).delete()
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Exception occurred on data save: {repr(e)}')