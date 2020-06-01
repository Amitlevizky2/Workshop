import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.DAL import Base, session
from project.DAL.DiscountORM import DiscountORM
from project.DAL.RegisteredUserORM import association_owners, association_managers

class ConditionalStoreDiscountORM(DiscountORM):
    __tablename__ = 'conditionalstorediscount'
    discount_id = Column(Integer, primary_key=True)
    store_id = Column(Integer,ForeignKey('stores.id'),primary_key=True)
    start_date = Column(datetime)
    end_dae = Column(datetime)
    precent = Column(Integer)
    min_price = Column(Integer)

    def min_price(self, id,min):
        update('conditionalstorediscount').where(discount_id=id).values(min_price=min)