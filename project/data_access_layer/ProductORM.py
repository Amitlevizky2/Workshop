from flask import Flask
from sqlalchemy import Table, Column, Integer, String, update, ForeignKey
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.domain_layer.stores_managment.Product import Product


def find_product(name, store_id):
    return session.query(ProductORM).filter_by(name=name, store_id=store_id).first()


def find_product_store_id(name, store_id):
    return session.query(ProductORM).filter_by(store_id=store_id).first()

class ProductORM(Base):
    __tablename__ = 'products'
    name = Column(String, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    categories = Column(String)
    key_words = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['products']], checkfirst=True)
        session.add(self)
        session.commit()

    def find_product(self, name, store_id):
        return session.query(ProductORM).filter_by(name=name, store_id=store_id).first()

    def update_product_amount(self, name, store_id, amount):
        update('products').where(name=name, store_id=store_id).value(quantity=amount)

    def update_product(self, name, store_id, attribute, updated):
        if attribute == self.categories:
            update('products').where(name=name, store_id=store_id).value(categories=updated)
        if attribute == self.key_words:
            update('products').where(name=name, store_id=store_id).value(key_words=updated)
        if attribute == self.price:
            update('products').where(name=name, store_id=store_id).value(price=updated)

    def delete(self):
        session.query(ProductORM).delete.where(name=self.name, store_id=self.store_id)

    def createObject(self):
        return Product(self.name, self.price, self.categorties, self.key_words, self.amount, self)