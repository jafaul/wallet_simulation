import uvicorn
from fastapi import FastAPI

from app.api import router
from app.database.models import TransferLog, Wallet

from app.database.database import engine, Base
from app.database.models.user import User
from config import config

app = FastAPI()

app.include_router(router.router)

if __name__ == '__main__':
    # table_objects = [TransferLog, User, Wallet]
    # for table_object in table_objects:
    #     if not engine.has_table(table_object.__tablename__):
    #         table_object.__table__.create(engine)
    # Base.metadata.create_all(engine, tables=table_objects, extend_existing=True)
    uvicorn.run("main:app", port=config.PORT, host=config.HOST, reload=True)