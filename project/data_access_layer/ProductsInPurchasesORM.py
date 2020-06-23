from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import session, Base, engine, proxy


class ProductsInPurchasesORM(Base):
    __tablename__ = 'productsinpurcases'
    purchase_id = Column(Integer, ForeignKey('purchases.id'), primary_key=True)
    product_name = Column(String, ForeignKey('products.name'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    quantity = Column(Integer)
    product = relationship("ProductORM")

    # create products in purchaseORM and send to this function
    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['productsinpurcases']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error


