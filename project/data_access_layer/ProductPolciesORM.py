import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from project.data_access_layer import Base, session, engine
from project.data_access_layer.PolicyORM import PolicyORM
from project.data_access_layer.ProductsInPoliciesORM import ProductsInPoliciesORM

class ProductPoliciesORM(PolicyORM):
    __tablename__ = 'productspolicies'
    policy_id = Column(Integer, ForeignKey('policies.policy_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    min_amount = Column(Integer)
    max_amount = Column(Integer)
    products = relationship("ProductsInPoliciesORM")
    __mapper_args__ = {
        'polymorphic_identity': 'Purchase Product Policy'
    }

    def update_min_amount(self, min):
        self.min_amount = min
        session.commit()

    def update_max_amount(self, id, max):
        self.max_amount =max
        session.commit()

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['productspolicies']], checkfirst=True)
        session.add(self)
        session.commit()

    def add_product(self, product_name):
        piporm = ProductsInPoliciesORM(policy_id=self.policy_id, product_name=product_name, store_id=self.store_id)
        piporm.add()

    def remove_product(self, product_name):
        session.query(ProductsInPoliciesORM).delete.where(policy_id=self.policy_id, product_name=product_name, store_id=self.store_id)
        session.commit()

    def createObject(self):
        from project.domain_layer.stores_managment.PurchasesPolicies.PurchaseProductPolicy import PurchaseProductPolicy
        poli = PurchaseProductPolicy(self.min_amout, self.max_amount, self.policy_id, self.store_id, self)
        prods = {}
        for piporm in self.products:
            prods[piporm.product_name] = True
        poli.products_in_policy = prods
        return poli