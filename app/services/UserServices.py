from fastapi import HTTPException, Depends

from app.Database import Database
from app.models.UsersModel import UsersModel
from typing import Annotated
from sqlalchemy.orm import Session
from app.schemas.UserUpdateSchema import UserUpdateSchema
from starlette import status


class UserServices:

    db_object = Database()
    db_dependency = Annotated[Session, Depends(db_object.get_db)]

    # get all users info
    def get_all_users(self,db:db_dependency):
        return db.query(UsersModel).all()

    # get user data by user_id
    def get_user_by_id(self,db:db_dependency,user_id:int):
        user_model = db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if user_model is not None:
            return user_model
        raise HTTPException(status_code=404, detail=f'can\'t load user with id: {user_id}')

    # Update customer data , excluding password
    # Admin role can be only assigned if is_admin = true
    def update_user(self,db:db_dependency,user_request:UserUpdateSchema,user_id, is_admin = False):
        if (
            user_request.username is None and
            user_request.email is None and
            user_request.first_name is None and
            user_request.last_name is None and
            user_request.role is None and
            user_request.phone_number is None
        ):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid request')
        user_model = db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if user_model is None:
            raise HTTPException(status_code=404, detail=f'can\'t load user with id: {user_id}')
        if user_request.role:
            if user_request.role == 'admin' and not is_admin:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Admin role assign permission require'
                )
            else:
                user_model.role = user_request.role
        if user_request.username:
            user_model.username = user_request.username
        if user_request.email:
            user_model.email = user_request.email
        if user_request.first_name:
            user_model.first_name = user_request.first_name
        if user_request.last_name:
            user_model.last_name = user_request.last_name
        if user_request.phone_number:
            user_model.phone_number = user_request.phone_number
        try:
            db.add(user_model)
            db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Exception occurred on data save: {repr(e)}'
            )
