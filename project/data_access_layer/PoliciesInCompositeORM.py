from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.ProductORM import ProductORM


class PoliciesInCompositeORM(Base):
    __tablename__ = 'Policy_in_composite'
    composite_discount_id = Column(Integer, ForeignKey('CompositePolicies.policy_id'), primary_key=True)
    policy_id = Column(Integer, ForeignKey('policies.policy_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    discount = relationship('PolicyORM', foreign_keys=[policy_id, store_id])

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['Policy_in_composite']], checkfirst=True)
        proxy.get_session().add(self)
        proxy.get_session().commit()