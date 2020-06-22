from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from project.data_access_layer.Proxy import Proxy

path = 'sqlite:///C:\\Users\\Lielle Ravid\\Desktop\\sixth semster\\sadna\\version 1\\project\\tradeSystem.db'
Base = declarative_base()
# session = sessionmaker()
engine = create_engine(path, echo = True)
# session.configure(bind=engine)
Session = sessionmaker(bind=engine)
# Session is a class
session = Session()
proxy = Proxy(session)
# Base.metadata.bind = engine
# Base.metadata.create_all(engine)
meta = MetaData()
meta.create_all(engine)
session.commit()
