from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String,update
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

def find_by_id(discount_id):
    session.query(DiscountORM).filter_by(discount_id=discount_id).first()


class DiscountORM(RegisteredUserORM):
    __tablename__ = 'discounts'
    discount_id = Column(Integer,primary_key=True)
    start_date = Column(datetime)
    end_date = Column(datetime)
    precent = Column(Integer)
    discounted =  relationship("ProductORM", secondary=assosiation_products,back_populates="name")
    discountin = relationship("StoreORM", secondary=assosiation_stores, back_populates="discount_id")

    def update_discount_precent(self,precent,id):
        update('discounts').where(discount_id=id).values(precent=precent)

    def update_start_date(self,id,start):
        update('discounts').where(discount_id=id).values(stat_date=start)

    def update_start_date(self,id,end):
        update('discounts').where(discount_id=id).values(end_date=end)
