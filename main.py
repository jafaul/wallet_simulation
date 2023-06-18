import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api import router
from app.database.models import TransferLog, Wallet

from app.database.database import engine, Base, url_object
from app.database.models.user import User
from config import config

app = FastAPI()

app.include_router(router.router)

if __name__ == '__main__':
    table_objects = [TransferLog.__table__, User.__table__, Wallet.__table__]
    Base.metadata.create_all(engine, tables=table_objects)

    # engine = create_engine(url_object)
    # Session = sessionmaker(bind=engine)
    # db = Session()
    #
    # # Test the connection by executing a simple query
    # users = db.query(User).all()
    # print(users)
    #
    # # Close the session
    # db.close()

    uvicorn.run("main:app", port=config.PORT, host=config.HOST, reload=True)