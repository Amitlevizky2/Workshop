import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from project.DAL import Base, session


class ProductPoliciesORM(Base):
    __tablename__ = 'productspolicies'
    policy_id = Column(Integer, primary_key=True)
    product_it = Column(Integer, ForeignKey('products.name'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    min_amout = Column(Integer)
    max_amount = Column(Integer)
    policy_in = relationship("ProductORM", back_populates="policy")

    def update_min_amount(self, id, min):
        update('storepolicys').where(policy_id=id).values(min_amount=min)

    def update_max_amount(self, id, max):
        update('storepolicys').where(policy_id=id).values(max_amount=max)
