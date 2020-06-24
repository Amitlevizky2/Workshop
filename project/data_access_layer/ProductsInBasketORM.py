from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.ProductORM import ProductORM


class ProductsInBasketORM(Base):
    __tablename__ = 'productsinbaskets'
    #basket_id = Column(Integer, ForeignKey('baskets.id'), primary_key=True)
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    product_name = Column(String, ForeignKey('products.name'), primary_key=True)
    quantity = Column(Integer)
    product = relationship("ProductORM")

    def update_quantity(self, amount):
        self.quantity = amount
        #proxy.get_session().commit()

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['productsinbaskets']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(type(e))
            return error

