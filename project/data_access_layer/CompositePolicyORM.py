from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.PolicyORM import PolicyORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine

policies_in_composite_association = Table('Policies_in_Composite', Base.metadata,
                             Column('composite_policy_id', Integer, ForeignKey('CompositePolicies.discount_id')),
                             Column('policy_id', Integer, ForeignKey('Policies.id'))
                             )



class CompositePolicyORM(PolicyORM):
    __tablename__ = 'CompositePolicies'
    id = Column(Integer, ForeignKey('discounts.id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('policies.id'), primary_key=True)
    logic_operator = Column(Integer)
    policies_in_here = relationship("PoliciesORM", secondary=policies_in_composite_association)

    def change_logic_operaor(self, id,store_id, lo):
        update('CompositeDiscounts').where(id=id, store_id=store_id).value(logic_operator=lo)

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['CompositePolicies']], checkfirst=True)
        session.add(self)
        session.commit()

    def add_policies(self, policies):
        for poli in policies:
            self.add_policy(poli)

    def add_policy(self, policy):
        pass
        #TODO: check how to add to association table

    def remove_policy(self, policy):
        pass
    #TODO: check association tables