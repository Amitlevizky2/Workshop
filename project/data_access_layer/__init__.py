from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

path = 'sqlite:///tradeSystem.db'
Base = declarative_base()
# session = sessionmaker()
engine = create_engine(path, echo = True)
# session.configure(bind=engine)
Session = sessionmaker(bind=engine)
# Session is a class
session = Session()

# Base.metadata.bind = engine
# Base.metadata.create_all(engine)
meta = MetaData()
meta.create_all(engine)
session.commit()
