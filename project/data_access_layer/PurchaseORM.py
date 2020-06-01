from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from project.data_access_layer import Base,session


class PurchaseORM(Base):
    __tablename__ = 'purchasess'
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    quantity = Column(Integer)
    date = Column(DateTime)

    def find_user_purchases(self, username):
        return session.query(PurchaseORM).filter_by(username=username)

    def find_store_purchases(self, store_id):
        return session.query(PurchaseORM).filter_by(store_id=store_id)

#create purchaseORM and send to this function
    def add(self, purchase):
        session.add(purchase)