from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.ProductORM import ProductORM


class PredicateORM(Base):
    __tablename__ = 'predicates'
    composite_discount_id = Column(Integer, ForeignKey('CompositeDiscounts.discount_id'), primary_key=True)
    discount_id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    product_name = Column(String, ForeignKey('products.name'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    ##not sure this works.
    product = relationship('ProductORM', foreign_keys=[product_name, store_id])
    discount = relationship('DiscountORM', back_populates='products', foreign_keys=[discount_id, store_id])

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['predicates']], checkfirst=True)
        session.add(self)
        session.commit()