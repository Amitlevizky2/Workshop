from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session
from project.data_access_layer.ProductORM import ProductORM


class ProductsInDiscountsORM(Base):
    __tablename__ = 'Discount_products'
    id = Column(Integer, primary_key=True)
    discount_id = Column(Integer, ForeignKey('discounts.discount_id'))
    product_name = Column(String, ForeignKey('products.name'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    ##not sure this works.
    product = relationship('ProductORM', foreign_keys=[product_name, store_id])
    discount = relationship('DiscountORM', back_populates='products')