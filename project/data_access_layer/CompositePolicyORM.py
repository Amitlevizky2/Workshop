from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.PolicyORM import PolicyORM
from project.data_access_layer.PoliciesInCompositeORM import PoliciesInCompositeORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine





class CompositePolicyORM(PolicyORM):
    __tablename__ = 'CompositePolicies'
    policy_id = Column(Integer, ForeignKey('policies.policy_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    logic_operator = Column(Integer)
    policies_to_apply = relationship("PoliciesInCompositeORM")

    def change_logic_operaor(self, lo):
        self.logic_operator = lo
        session.commit()

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['CompositePolicies']], checkfirst=True)
        session.add(self)
        session.commit()

    def add_policies(self, purchase_policies):
        for policy in purchase_policies:
            from project.data_access_layer.PoliciesInCompositeORM import PoliciesInCompositeORM
            poliorm = PoliciesInCompositeORM(composite_discount_id = self.policy_id, policy_id = policy.id, store_id = self.store_id)
            poliorm.add()
