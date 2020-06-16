from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session,engine
from project.data_access_layer.ProductORM import ProductORM
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM
from project.data_access_layer.StoreORM import StoreORM


class Handler:
    def __init__(self):
        session
        #init db tables?
        #open session

    def find_user(self, username):
        user = session.query(RegisteredUserORM).filter_by(username=username)
        return user.createObject()

    def find_store(self, store_id):
        store = session.query(StoreORM).filter_by(id=store_id)
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
            real_users.append(user.createObject)


    def search(self, name):
        #maybe filter like
        products = session.query(ProductORM).fiter_by(name=name)
        real_products =[]
        prod_discounts = {} #{store_id, [discounts]}
        for product in products:
            real_products.append(product.createObject())
            discounts = session.query(ProductsInDiscountsORM).filter_by(product_name=name)
            prod_discounts[product.store_id] = []
            for dis in discounts:
                real_discount = dis.createObject()
                prod_discounts[product.store_id].append(real_discount)
        # what to return the products? or the discounts?
