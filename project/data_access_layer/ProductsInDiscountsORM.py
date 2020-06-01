from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session


class ProductsInDiscountsORM(Base):
    __tablename__ = 'Discount_products'
    id = Column('id', Integer, primary_key=True)
    discount_id = Column('discount_id', Integer, ForeignKey('discounts.discount_id'))
    product_name = Column(String, ForeignKey('products.name'))
    store_id = Column('store_id', Integer, ForeignKey('products.store_id'))
    ##not sure this works.
    product = relationship('ProductORM', back_populates='discounts')
    discount = relationship('DiscountORM', back_populates='products')