from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session




class PolicyORM(Base):
    __tablename__ = 'Policies'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
