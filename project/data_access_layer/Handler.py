from datetime import date

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.ProductORM import ProductORM
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM
from project.data_access_layer.PurchaseORM import PurchaseORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM
from project.data_access_layer.StatsORM import StatsORM
from project.data_access_layer.StoreORM import StoreORM
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from project.data_access_layer.Proxy import Proxy

class Handler:
    def __init__(self, publisher):
        self.publisher = publisher

    def init_db(self):
        path = 'sqlite:///C:\\Users\\Lielle Ravid\\Desktop\\sixth semster\\sadna\\version 1\\project\\tradeSystem.db'
        global Base
        Base = declarative_base()
        # session = sessionmaker()
        engine = create_engine(path, echo=True)
        # session.configure(bind=engine)
        Session = sessionmaker(bind=engine)
        # Session is a class
        session = Session()
        proxy = Proxy(session)
        # Base.metadata.bind = engine
        # Base.metadata.create_all(engine)
        meta = MetaData()
        meta.create_all(engine)
        session.commit()

    def find_user(self, username):
        user = proxy.get_handler_session().query(RegisteredUserORM).filter_by(username=username).first()
        return user.createObject()

#CALL WHEN ADDED TO CART PRODUCT
    def find_store(self, store_id):
        store = proxy.get_handler_session().query(StoreORM).filter_by(id=store_id).first()
        return store.createObject()

    def get_all_stores(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
        stores = proxy.get_handler_session().query(StoreORM)
        real_stores = []
        for store in stores:
            real_stores.append(store.createObject())
        return real_stores

    def get_all_regusers(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['notifications']], checkfirst=True)
        users = proxy.get_handler_session().query(RegisteredUserORM)
        real_users =[]
        for user in users:
            real_users.append(user.createObject())
        return real_users

    def search(self, name):
        #maybe filter like
        #CHECK HOW TO QUERY CONTAINS
        products = proxy.get_handler_session().query(ProductORM).fiter_by(name="%name%")
        real_products =[]
        prod_discounts = {}
        result={}
        for product in products:
            storeorm = proxy.get_handler_session().query(StoreORM).filter_by(id=product.store_id)
            store_name = storeorm.name
            if store_name not in result.keys():
                result[store_name] = {"products": [], "discounts": []}
            result[store_name]["products"].append(product.createObject())
            pidOrm = proxy.get_handler_session().query(ProductsInDiscountsORM).filter_by(product_name=name, store_id =product.store_id)
            for dis in pidOrm:
                real_discount = dis.discount.createObject()
                result[store_name]["discounts"].append(real_discount)
        return result
        #return list of  {store_name, {products:[Products], discounts:[Discounts] } }

    def find_user_purchases(self, username):
        orms = proxy.get_handler_session().query(PurchaseORM).filter_by(username=username)
        purchases = []
        for p in orms:
            purchase = p.createObject()
            purchases.append(purchase)
        return purchases

    def find_store_purchases(self, store_id):
        orms = proxy.get_handler_session().query(PurchaseORM).filter_by(store_id=store_id)
        purchases =[]
        for p in orms:
            purchase = p.createObject()
            purchases.append(purchase)
        return purchases

    def is_admin(self, username):
        userorm = proxy.get_handler_session().query(RegisteredUserORM).filter_by(username=username)
        return userorm.admin is 1
#TODO:
    #def buy(self):

    #def viewcart(self, username):

    def get_admins(self):
        admin = proxy.get_handler_session().query(RegisteredUserORM).filter_by(admin=1)
        admins =[]
        for ad in admin:
            admins.append(ad.username)
        return admins

    def get_stats(self):
        from project.domain_layer.users_managment.Statistics import Statistics
        Base.metadata.create_all(engine, [Base.metadata.tables['stats']], checkfirst=True)
        stats = {}
        res = proxy.get_session().query(StatsORM)
        for stat in res:
            stats[stat.date] = {'guests': stat.guests,
                                'registered_users': stat.reg_users,
                                'managers': stat.managers,
                                'owners': stat.owners}
        today = str(date.today())
        orm_today = proxy.get_session().query(StatsORM).filter_by(date=today).first()
        stat = Statistics(orm_today)
        stat.set_publisher(self.publisher)
        return stat

    def get_store_index(self):
        index = proxy.get_session().query(StoreORM).count()
        return index
