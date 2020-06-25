from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean

from project.data_access_layer import session, Base, engine



class ProductsInPurchasesORM(Base):
    __tablename__ = 'productsinpurcases'
    purchase_id = Column(Integer, ForeignKey('purchases.id'), primary_key=True)
    product_name = Column(String, ForeignKey('products.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    quantity = Column(Integer)

    # create products in purchaseORM and send to this function
    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['productsinpurcases']], checkfirst=True)
        session.add(self)
        session.commit()
