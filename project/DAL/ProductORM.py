from flask import Flask
from sqlalchemy import Table, Column, Integer, String
from project.DAL import Base, session


def find_product(name, store_id):
    return session.query(ProductORM).filter_by(name=name, store_id=store_id).first()


def find_product_store_id(name, store_id):
    return session.query(ProductORM).filter_by(store_id=store_id).first()

class ProductORM(Base):
    __tablename__ = 'products'
    name = Column(String, primary_key=True)
    store_id = Column(Integer, primary_key=True)
    categories = Column(String)
    key_words = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)

def find_product(name, store_id):
    return session.query(ProductORM).filter_by(name= name, store_id=store_id).first()