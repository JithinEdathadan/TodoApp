from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from TodoApp.models.base import Base
from TodoApp.Settings import get_settings
# import TodoApp.models # This triggers the import of all model classes
settings = get_settings()
class Database:
    def __init__(self):
        SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USER_NAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.session_local = sessionmaker(autoflush=False, autocommit= False, bind=self.engine)
        self.Base = Base
    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)
# session_local = sessionmaker(autoflush=False, autocommit= False, bind=engine)
# Base = declarative_base()
#
# def get_db():
#     db =session_local()
#     try:
#         yield db
#     finally:
#         db.close()