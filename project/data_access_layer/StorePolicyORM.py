import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.PolicyORM import PolicyORM


class StorePolicyORM(PolicyORM):
    __tablename__ = 'storepolicies'
    policy_id = Column(Integer, ForeignKey('policies.policy_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    min_amount = Column(Integer)
    max_amount = Column(Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'store_policy',
    }


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['storepolicies']], checkfirst=True)
        session.add(self)
        session.commit()

    def update_min_amount(self, id, min):
        self.min_amount = min
        session.commit()

    def update_max_amount(self, id, max):
        self.max_amount = max
        session.commit()