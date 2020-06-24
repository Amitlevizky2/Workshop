import jsons
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.domain_layer.external_managment.Purchase import Purchase


class PurchaseORM(Base):
    __tablename__ = 'purchases'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    date = Column(DateTime, primary_key=True)
    id = Column(Integer)
    products = Column(Text)


#create purchaseORM and send to this function
    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['purchases']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(type(e))
            return error


    def createObject(self):
        return Purchase(jsons.loads(self.products), self.username, self.store_id, self.id, self)