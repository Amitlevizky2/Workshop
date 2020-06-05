from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update

from project.data_access_layer import Base, session, engine


class ProductsInBasketORM(Base):
    __tablename__ = 'productsinbaskets'
    basket_id = Column(Integer, ForeignKey('baskets.id'), primary_key=True)
    product_name = Column(String, ForeignKey('products.username'), primary_key=True)
    quantity = Column(Integer)

    def update_quantity(self, id, product_name, amount):
        update('productsinbaskets').where(basket_id=id, product_name=product_name).values(quantity=amount)
        session.commit()

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['productsinbaskets']], checkfirst=True)
        session.add(self)
        session.commit()
