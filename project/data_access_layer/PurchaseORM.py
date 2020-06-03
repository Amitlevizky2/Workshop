from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from project.data_access_layer import Base,session
from project.data_access_layer.ProductsInPurchasesORM import ProductsInPurchasesORM


class PurchaseORM(Base):
    __tablename__ = 'purchasess'
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    date = Column(DateTime)

    def find_user_purchases(self, username):
        return session.query(PurchaseORM).filter_by(username=username)

    def find_store_purchases(self, store_id):
        return session.query(PurchaseORM).filter_by(store_id=store_id)

#create purchaseORM and send to this function
    def add(self):
        session.add()

    def add_products_to_purchase(self, products):
        for product in products:
            productinpurchase = ProductsInPurchasesORM(purchase_id=self.id, product_name=product.product_name, store_id=product.store_id, quantity = pquantity)
            session.add(productinpurchase)
            session.commit()