import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import association_owners, association_managers

class ConditionalStoreDiscountORM(DiscountORM):
    __tablename__ = 'conditionalstorediscounts'
    discount_id = id = Column(Integer, ForeignKey('discounts.id'), primary_key=True)
    store_id = Column(Integer,ForeignKey('stores.id'),primary_key=True)
    min_price = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'ConditionalStore',
    }

    def Update_min_price(self, id, min):
        update('conditionalstorediscount').where(discount_id=id).values(min_price=min)

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['conditionalstoredicounts']], checkfirst=True)
        session.add(self)
        session.commit()