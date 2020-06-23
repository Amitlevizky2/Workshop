from flask import Flask
from sqlalchemy import Table, Column, Integer, String, update, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.domain_layer.stores_managment.Product import Product


def find_product(name, store_id):
    return proxy.get_session().query(ProductORM).filter_by(name=name, store_id=store_id).first()


def find_product_store_id(name, store_id):
    return proxy.get_session().query(ProductORM).filter_by(store_id=store_id).first()

class ProductORM(Base):
    __tablename__ = 'products'
    name = Column(String, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    categories = Column(String)
    key_words = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)


    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['products']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error


    def find_product(self, name, store_id):
        return proxy.get_session().query(ProductORM).filter_by(name=name, store_id=store_id).first()

    def update_product_amount(self, amount):
        self.quantity = amount
        proxy.get_session().commit()

    def update_product(self, attribute, updated):
        if attribute == self.categories:
            self.categories = updated
        if attribute == self.key_words:
            self.key_words = updated
        if attribute == self.price:
            self.price = updated
        proxy.get_session().commit()

    def delete(self):
        proxy.get_session().delete(self)
        proxy.get_session().commit()

    def createObject(self):
        return Product(self.name, self.price, self.categories, self.key_words, self.quantity, self.store_id, self)