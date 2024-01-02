from fastapi import FastAPI
from . import config
from app.users.routers.user_routes import api_router as user_router
from cassandra.cqlengine.management import sync_table
import db, pathlib
from app.users.models import User


DB_SESSION = None

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "templates"


# settings = config.get_settings()
def get_app():
    app = FastAPI(version="0.0.1")
    

    app.include_router(user_router)

    @app.on_event("startup")
    def startup():
        global DB_SESSION
        DB_SESSION = db.get_session()
        sync_table(User)

        print(BASE_DIR)

    return app
