from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.DAL import Base


class ProductORM(Base):
    __tablename__ = 'products'
    name = Column(String, primary_key=True)
    store_id = Column(Integer, primary_key=True)
    categories = Column(String)
    key_words = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)