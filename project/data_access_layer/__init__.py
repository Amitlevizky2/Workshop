from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


path = 'sqlite:///C:\\Users\\Lielle Ravid\\Desktop\\sixth semster\\sadna\\version 1'
Base = declarative_base()
session = sessionmaker()
engine = create_engine(path)
session.configure(bind=engine)