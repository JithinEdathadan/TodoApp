from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from TodoApp.models.base import Base
# import TodoApp.models # This triggers the import of all model classes

class Database:
    def __init__(self):
        sql_file_name = "database.db"
        connect_args = {"check_same_thread": False}
        self.sqlite_url = f"sqlite:///{sql_file_name}"
        self.engine = create_engine(self.sqlite_url, connect_args=connect_args)
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