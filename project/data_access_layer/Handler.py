from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session,engine
from project.data_access_layer.ProductORM import ProductORM
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM
from project.data_access_layer.PurchaseORM import PurchaseORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM
from project.data_access_layer.StoreORM import StoreORM


class Handler:
    def __init__(self):
        session
        #init db tables?
        #open session

    def find_user(self, username):
        user = session.query(RegisteredUserORM).filter_by(username=username).first()
        return user.createObject()

#CALL WHEN ADDED TO CART PRODUCT
    def find_store(self, store_id):
        store = session.query(StoreORM).filter_by(id=store_id).first()
        return store.createObject()

    def get_all_stores(self):
        stores = session.query(StoreORM)
        real_stores = []
        for store in stores:
            real_stores.append(store.createObject())

    def get_all_regusers(self):
        users = session.query(RegisteredUserORM)
        real_users =[]
        for user in users:
            real_users.append(user.createObject())

    def search(self, name):
        #maybe filter like
        #CHECK HOW TO QUERY CONTAINS
        products = session.query(ProductORM).fiter_by(name="%name%")
        real_products =[]
        prod_discounts = {}
        result={}
        for product in products:
            storeorm = session.query(StoreORM).filter_by(id=product.store_id)
            store_name = storeorm.name
            if store_name not in result.keys():
                result[store_name] = {"products": [], "discounts": []}
            result[store_name]["products"].append(product.createObject())
            pidOrm = session.query(ProductsInDiscountsORM).filter_by(product_name=name, store_id =product.store_id)
            for dis in pidOrm:
                real_discount = dis.discount.createObject()
                result[store_name]["discounts"].append(real_discount)
        return result
        #return list of  {store_name, {products:[Products], discounts:[Discounts] } }

    def find_user_purchases(self, username):
        return session.query(PurchaseORM).filter_by(username=username)

    def find_store_purchases(self, store_id):
        return session.query(PurchaseORM).filter_by(store_id=store_id)


#TODO:
    #def buy(self):


    #def login(self,username):


    #def viewcart(self, username):