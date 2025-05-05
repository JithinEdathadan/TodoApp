from datetime import datetime, timezone
from datetime import timedelta

from fastapi import HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.Database import Database
from app.schemas.UserSchema import UserSchema
from jose import jwt,JWTError
from app.models.UsersModel import UsersModel
from passlib.context import CryptContext
from starlette import status

from app.Settings import get_settings

from app.schemas.AuthChangePasswordSchema import AuthChangePasswordSchema


bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

settings = get_settings()

class AuthServices:
    db_object = Database()
    db_dependency = Annotated[Session, Depends(db_object.get_db)]

    def create_user(self,db:db_dependency,user_data:UserSchema,is_admin):
        if user_data.role == "admin" and not is_admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Admin role creation is not permitted')
        try:
            # user_data_object = UsersModel(**user_data.model_dump()) this will not work as the password and hashed password fields are different
            user_data_object = UsersModel(
                username = user_data.username,
                email = user_data.email,
                first_name = user_data.first_name,
                last_name = user_data.last_name,
                hashed_password = bcrypt_context.hash(user_data.password),
                user_role = user_data.role,
                is_active = True,
                phone_number = user_data.phone_number
            )
            db.add(user_data_object)
            db.commit()
            return {
                "status":True
            }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Can\'t create user : {repr(e)}')
    def authenticate_user(self,db:db_dependency,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
        user = db.query(UsersModel).filter(UsersModel.username == form_data.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
        if not bcrypt_context.verify(form_data.password,user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
        token = self.create_access_token(form_data.username,user.id,user.user_role,timedelta(minutes=settings.JWT_TOKEN_EXPIRY))
        return {
            'access_token':token,
            'token_type':'bearer'
        }


    def create_access_token(self,username:str,user_id:int,role:str,expires_delta:timedelta):
        encode = {
            'sub':username,
            'id':user_id,
            'role':role
        }
        expires = datetime.now(timezone.utc)+expires_delta
        encode.update(
            {
                'exp':expires
            }
        )
        return jwt.encode(encode,settings.SECRET_KEY,settings.ALGORITHM)

    def reset_password(self,db:db_dependency,passwords:AuthChangePasswordSchema,user_id:int):
        user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'unable to load user : {user_id}')
        if not bcrypt_context.verify(passwords.password,user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
        user.hashed_password = bcrypt_context.hash(passwords.new_password)
        try:
            db.add(user)
            db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Exception occurred on data save: {repr(e)}'
            )

    async def get_current_user(self,token:Annotated[str , Depends(oauth2_bearer)]):
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
            username:str = payload.get('sub')
            user_id:int = payload.get('id')
            user_role:str = payload.get('role')
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed 1")
            return {
                "username":username,
                "id":user_id,
                "user_role":user_role
            }
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Authentication failed {repr(e)}')

    async def is_current_user_admin(self,token:Annotated[str , Depends(oauth2_bearer)]):
        if token is None:
            return False
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
            user_role:str = payload.get('role')
            if user_role == "admin":
                return True
            return False
        except JWTError:
            return False



