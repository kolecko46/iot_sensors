import modules.config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

def check_db_connection(database):
    try:
        database.execute("SELECT 1")
        return True
    except: 
        return False