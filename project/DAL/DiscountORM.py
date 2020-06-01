from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import  datetime
from project.DAL.RegisteredUserORM import RegisteredUserORM

from project.DAL import Base,session

assosiation_products = Table('Discount_products', Base.metadata,
                             Column('discount_id',Integer,ForeignKey('discounts.discount_id')),
                             Column('start_date',datetime,ForeignKey('discounts.start_date')),
                             Column('end_date', datetime, ForeignKey('discounts.end_date')),
                             Column('precent',Integer,ForeignKey('discounts.precent')),
                             Column('store_id', Integer, ForeignKey('stores.id'))
                             )

assosiation_stores = Table('store_discounts', Base.metadata,
                           Column('discount_id', Integer, ForeignKey('discounts.discount_id')),
                           Column('start_date', datetime, ForeignKey('discounts.start_date')),
                           Column('end_date', datetime, ForeignKey('discounts.end_date')),
                           Column('precent', Integer, ForeignKey('discounts.precent')),
                           Column('store_id', Integer, ForeignKey('stores.id'))
                           )

class DiscountORM(RegisteredUserORM):
    __tablename__ = 'discounts'
    discount_id = Column(Integer,primary_key=True)
    start_date = Column(datetime)
    end_dae = Column(datetime)
    precent = Column(Integer)
    discounted =  relationship("ProductORM", secondary=assosiation_products,back_populates="name")
    discountin = relationship("StoreORM", secondary=assosiation_stores, back_populates="discount_id")