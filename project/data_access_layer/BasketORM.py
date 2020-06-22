
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, text
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.ProductsInBasketORM import ProductsInBasketORM





class BasketORM(Base):
    __tablename__ = 'baskets'
    #id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    user = relationship("RegisteredUserORM", back_populates="baskets")

    def find_user_baskets(self, username):
        return proxy.get_session().query(BasketORM).filter_by(username=username).first()



    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['baskets']], checkfirst=True)
        proxy.get_session().add(self)
        proxy.get_session().commit()


    #add commit
    #update quantity for adding and removing
    def update_basket_product_quantity(self, product_name, amount):
        piborm = proxy.get_session().query(ProductsInBasketORM).filter_by(username=self.username, store_id=self.store_id, product_name=product_name).first()
        piborm.update_quantity(amount)
       # ProductsInBasketORM.update_quantity(self.username, self.store_id, product_name, amount)

    def update_basket_add_product(self, product_name, amount):
        productinbasket = ProductsInBasketORM(username= self.username, store_id=self.store_id, product_name = product_name, quantity = amount)
        productinbasket.add()


    def remove_product_from_basket(self, product_name):
        proxy.get_session().query(ProductsInBasketORM).delete.where(username= self.username, store_id=self.store_id, product_name=product_name)
        proxy.get_session().commit()

    def remove_basket(self):
        proxy.get_session().query(ProductsInBasketORM).delete.where(username= self.username, store_id=self.store_id)
        proxy.get_session().query(BasketORM).delete.where(username= self.username, store_id=self.store_id)
        proxy.get_session().commit()

    def createObject(self):
        from project.domain_layer.users_managment.Basket import Basket
        basket = Basket(self.username, self.store_id, self)
        products = proxy.get_session().query(ProductsInBasketORM).filter_by(username= self.username, store_id=self.store_id)
        prods ={}
        for product in products:
            prods[product.product.name] = product.product.quantity
        basket.products = prods
        return basket