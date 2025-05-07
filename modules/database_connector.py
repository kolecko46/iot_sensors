import modules.config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False,
                             autoflush=False,
                             bind=engine)

def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()

def check_db_connection(db):
    try:
        db.execute(text("SELECT 1"))
        return ('ok')
    except SQLAlchemyError as e: 
        print(e)
        return ('no_response')