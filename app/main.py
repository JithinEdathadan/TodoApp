from fastapi import FastAPI
from app.Database import Database
from app.routers import ToDosRoutes,AuthRoutes,AdminToDosRoutes, UserRoutes, AdminUsersRoutes

class Main:
    def __init__(self):
        self.app = FastAPI()
        self._setup_database()
        self._include_routers()

    def _setup_database(self):
        db_object = Database()
        # Create tables if they don't exist
        db_object.Base.metadata.create_all(bind=db_object.engine)

    def _include_routers(self):
        self.app.include_router(AuthRoutes.router)
        self.app.include_router(ToDosRoutes.router)
        self.app.include_router(UserRoutes.router)
        self.app.include_router(AdminToDosRoutes.router)
        self.app.include_router(AdminUsersRoutes.router)


    def get_app(self):
        return self.app


# Create an instance of the app
app = Main().get_app()
