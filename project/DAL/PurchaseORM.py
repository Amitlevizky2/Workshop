from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from project.DAL import Base


class PurchaseORM(Base):
    __tablename__ = 'purchasess'
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    quantity = Column(Integer)
    date = Column(DateTime)