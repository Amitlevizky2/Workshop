import jsons
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.ProductsInPurchasesORM import ProductsInPurchasesORM
from project.domain_layer.external_managment.Purchase import Purchase


class PurchaseORM(Base):
    __tablename__ = 'purchases'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    date = Column(DateTime, primary_key=True)
    id = Column(Integer)


#create purchaseORM and send to this function
    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['purchases']], checkfirst=True)
        session.add(self)
        session.commit()

    def createObject(self):
        return Purchase(jsons.loads(self.products), self.username, self.store_id, self.id, self)