from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.DAL import Base


class BasketORM(Base):
    __tablename__ = 'baskets'
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    #not sure if needed
    total_price = Column(Integer)