from sqlalchemy.orm import Session

from database.database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def get_db():
#     db: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     try:
#         yield db
#     finally:
#         db.close()