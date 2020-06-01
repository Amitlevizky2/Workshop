import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from project.DAL.DiscountORM import DiscountORM
from project.DAL.RegisteredUserORM import association_owners, association_managers


class ConditionalDiscountsORM(DiscountORM):
    __tablename__ = 'conditionalproductdiscounts'
    discount_id = Column(Integer, primary_key=True)
    product_id = Column(String,ForeignKey('products.name'), primary_key=True)
    start_date = Column(datetime)
    end_dae = Column(datetime)
    precent = Column(Integer)
    min_amount = Column(Integer)
    num_products_to_apply = Column(Integer)

    def update_min_amount(self,id,min):
        update('conditionalproductdiscounts').where(discount_id=id).values(min_amount=min)

    def update_num_to_apply(self,id,num):
        update('conditionalproductdiscounts').where(discount_id=id).values(num_products_to_apply=num)

