from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.ProductORM import ProductORM


class DiscountToApplyORM(Base):
    __tablename__ = 'to_apply_composite'
    composite_discount_id = Column(Integer, ForeignKey('CompositeDiscounts.discount_id'), primary_key=True)
    discount_id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    discount = relationship('DiscountORM', foreign_keys=[discount_id, store_id])

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['to_apply_composite']], checkfirst=True)
        session.add(self)
        session.commit()