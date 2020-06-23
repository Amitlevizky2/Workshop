import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer import PolicyORM


class StorePolicyORM(Base):
    __tablename__ = 'storepolicies'
    policy_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    min_amount = Column(Integer)
    max_amount = Column(Integer)


    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
            Base.metadata.create_all(engine, [Base.metadata.tables['storepolicies']], checkfirst=True)
            PolicyORM.add(self.policy_id, self.store_id)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error


    def update_min_amount(self, id, min):
        self.min_amount = min
        proxy.get_session().commit()

    def update_max_amount(self, id, max):
        self.max_amount = max
        proxy.get_session().commit()

    def createObject(self):
        from project.domain_layer.stores_managment.PurchasesPolicies.PurchaseStorePolicy import PurchaseStorePolicy
        real = PurchaseStorePolicy(self.min_amount, self.max_amount, self.policy_id, self.store_id, self)
        prods={}
        from project.data_access_layer.ProductsInPoliciesORM import ProductsInPoliciesORM
        res = proxy.get_session().query(ProductsInPoliciesORM).filter(ProductsInPoliciesORM.policy_id==self.policy_id).filter(ProductsInPoliciesORM.store_id==self.store_id)
        for piporm in res:
            prods[piporm.product_name] = True
        real.products_in_policy = prods
        return real

