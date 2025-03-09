import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

user_name = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
host = os.environ.get('MYSQL_HOST')
database_name = os.environ.get('MYSQL_DATABASE')

DATABASE = f'mysql+mysqlconnector://{user_name}:{password}@{host}/{database_name}?charset=utf8'

ENGINE = create_engine(DATABASE, echo=True, pool_recycle=3600)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE, expire_on_commit=False))

Base = declarative_base()
