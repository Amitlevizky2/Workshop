from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String,update
from sqlalchemy.orm import relationship
from datetime import  datetime

from project.data_access_layer import Base, session
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM


def find_by_id(discount_id):
    session.query(DiscountORM).filter_by(discount_id=discount_id).first()


class DiscountORM(Base):
    __tablename__ = 'discounts'
    discount_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    #MODIFY TO STRING
    start_date = Column(String)
    end_date = Column(String)
    precent = Column(Integer)
    products = relationship("ProductsInDiscountsORM")
    discriminator = Column('type', String(50))
    #store = relationship("StoreORM", back_populates="discounts")
    __mapper_args__ = {
        'polymorphic_identity': 'discount',
        'polymorphic_on': discriminator
    }

    def update_discount_precent(self, precent, id):
        update('discounts').where(discount_id=id).values(precent=precent)

    def update_start_date(self, id, start):
        update('discounts').where(discount_id=id).values(stat_date=start)

    def update_end_date(self,id,end):
        update('discounts').where(discount_id=id).values(end_date=end)
