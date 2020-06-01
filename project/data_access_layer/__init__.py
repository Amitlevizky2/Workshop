from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
session = sessionmaker()
engine = create_engine('sqlite://')
session.configure(bind=engine)