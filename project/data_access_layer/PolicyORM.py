from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine


class PolicyORM(Base):
    __tablename__ = 'policies'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        session.add(self)
        session.commit()