from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session

predicates_association = Table('Predicates', Base.metadata,
                               Column('composite_discount_id', Integer, ForeignKey('CompositeDiscounts.discount_id')),
                               Column('discount_product_id', Integer, ForeignKey('Discount_products.id'))
                               )

to_apply_association = Table('To_apply', Base.metadata,
                             Column('composite_discount_id', Integer, ForeignKey('CompositeDiscounts.discount_id')),
                             Column('discount_id', Integer, ForeignKey('Discounts.id'))
                             )


def find_by_id(discount_id):
    session.query(DiscountORM).filter_by(discount_id=discount_id).first()


class CompositeDiscountORM(DiscountORM):
    __tablename__ = 'CompositeDiscounts'
    discount_id = Column(Integer, ForeignKey('discounts.id'), primary_key=True)
    logic_operator = Column(Integer)
    products_in_predicates = relationship("ProductInDiscountsORM", secondary=predicates_association)
    discounts_to_apply = relationship("DiscountORM", secondary=to_apply_association)


    __mapper_args__ = {
        'polymorphic_identity': 'CompositeDiscount',
    }

    def change_logic_operaor(self,id,lo):
        update('CompositeDiscounts').where(discount_id = id).value(logic_operator = lo)

