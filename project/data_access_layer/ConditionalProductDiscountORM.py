import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, engine, session
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import association_owners, association_managers


class ConditionalProductDiscountsORM(DiscountORM):
    __tablename__ = 'conditionalproductdiscounts'
    discount_id = Column(Integer, ForeignKey('discounts.id'), primary_key=True)
    product_id = Column(String, ForeignKey('products.name'), primary_key=True)
    num_products_to_apply = Column(Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'ConditionalProduct',
    }

    def update_min_amount(self,id,min):
        update('conditionalproductdiscounts').where(discount_id=id).values(min_amount=min)

    def update_num_to_apply(self,id,num):
        update('conditionalproductdiscounts').where(discount_id=id).values(num_products_to_apply=num)


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['conditionalproductdiscounts']], checkfirst=True)
        session.add(self)
        session.commit()