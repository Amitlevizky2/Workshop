
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, text
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.ProductsInBasketORM import ProductsInBasketORM





class BasketORM(Base):
    __tablename__ = 'baskets'
    #id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    user = relationship("RegisteredUserORM", back_populates="baskets")

    def find_user_baskets(self, username):
        return session.query(BasketORM).filter_by(username=username).first()



    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['baskets']], checkfirst=True)
        session.add(self)
        session.commit()


    #add commit
    #update quantity for adding and removing
    def update_basket_product_quantity(self, product_name, amount):
        piborm = session.query(ProductsInBasketORM).filter_by(username=self.username, store_id=self.store_id, product_name=product_name).first()
        piborm.update_quantity(amount)
       # ProductsInBasketORM.update_quantity(self.username, self.store_id, product_name, amount)

    def update_basket_add_product(self, product_name, amount):
        productinbasket = ProductsInBasketORM(username= self.username, store_id=self.store_id, product_name = product_name, quantity = amount)
        productinbasket.add()


    def remove_product_from_basket(self, product_name):
        session.query(ProductsInBasketORM).delete.where(username= self.username, store_id=self.store_id, product_name=product_name)
        session.commit()

    def remove_basket(self):
        session.query(ProductsInBasketORM).delete.where(username= self.username, store_id=self.store_id)
        session.query(BasketORM).delete.where(username= self.username, store_id=self.store_id)
        session.commit()

    def createObject(self):
        from project.domain_layer.users_managment.Basket import Basket
        basket = Basket(self.username, self.store_id, self)
        products = session.query(ProductsInBasketORM).filter_by(username= self.username, store_id=self.store_id)
        prods ={}
        for product in products:
            prods[product.name] = product.amount
        basket.products = prods
        return basket