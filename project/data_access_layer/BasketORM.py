from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session
from project.data_access_layer.ProductsInBasketORM import ProductsInBasketORM





class BasketORM(Base):
    __tablename__ = 'baskets'
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    #not sure if needed

    def find_user_baskets(self, username):
        return session.query(BasketORM).filter_by(username=username).first()


    #add commit
    def add(self, basket):
        session.add(basket)


    #add commit
    #update quantity for adding and removing
    def update_basket_product_quantity(self, product_name, amount):
        ProductsInBasketORM.update_quantity(self.id, product_name, amount)

#add commit
    def update_basket_add_product(self, product_name, amount):
        productinbasket = ProductsInBasketORM(basket_id = self.id, product_name = product_name, quantity = amount)
        session.add(productinbasket)

#add commit?
    def remove_product_from_basket(self, product_name):
        session.query(ProductsInBasketORM).delete.where(basket_id=self.id, product_name=product_name)

    def remove_basket(self):
        session.query(ProductsInBasketORM).delete.where(basket_id = self.id)
        session.query(BasketORM).delete.where(id=self.id)
        #session.commit()