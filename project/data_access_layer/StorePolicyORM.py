import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.PolicyORM import PolicyORM


class StorePolicyORM(PolicyORM):
    __tablename__ = 'storepolicies'
    policy_id = Column(Integer, ForeignKey('policies.policy_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    min_amount = Column(Integer)
    max_amount = Column(Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'Store Policy'
    }


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['storepolicies']], checkfirst=True)
        proxy.get_session().add(self)
        proxy.get_session().commit()

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
        for piporm in self.products:
            prods[piporm.product_name] = True
        real.products_in_policy = prods
        return real

