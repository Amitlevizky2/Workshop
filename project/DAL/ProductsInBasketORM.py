from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from project.DAL.RegisteredUserORM import RegisteredUserORM


class ProductsInBasketORM(RegisteredUserORM):
    __tablename__ = 'productsinbaskets'
    basket_id = Column(Integer, ForeignKey('baskets.id'), primary_key=True)
    product_name = Column(String, ForeignKey('products.username'), primary_key=True)
    quantity = Column(Integer)