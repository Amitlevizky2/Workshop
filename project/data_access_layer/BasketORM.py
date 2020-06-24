
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, text
from sqlalchemy.exc import SQLAlchemyError
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


#sqlalchemy.exc.IntegrityError
    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['baskets']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(type(e))
            return error


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
        res = proxy.get_session().query(ProductsInBasketORM).filter_by(username= self.username, store_id=self.store_id, product_name=product_name).first()
        proxy.get_session().delete(res)
        proxy.get_session().commit()

    def remove_basket(self):
        res = proxy.get_session().query(ProductsInBasketORM).filter_by(username= self.username, store_id=self.store_id).first()
        for piborm in res:
            proxy.get_session().delete(piborm)
            proxy.get_session().commit()
        proxy.get_session().delete(self)
        proxy.get_session().commit()

    def createObject(self):
        from project.domain_layer.users_managment.Basket import Basket
        basket = Basket(self.username, self.store_id, self)
        Base.metadata.create_all(engine, [Base.metadata.tables['productsinbaskets']], checkfirst=True)
        products = proxy.get_session().query(ProductsInBasketORM).filter_by(username= self.username, store_id=self.store_id)
        prods ={}
        for product in products:
            prods[product.product.name] = product.product.quantity
        basket.products = prods
        return basket