from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine

predicates_association = Table('Predicates', Base.metadata,
                               Column('composite_discount_id', Integer, ForeignKey('CompositeDiscounts.discount_id')),
                               Column('discount_id', Integer, ForeignKey('discounts.discount_id')),
                               Column('product_name', String, ForeignKey('products.name')),
                               Column('store_id', Integer, ForeignKey('stores.id'))
                               )

to_apply_association = Table('To_apply', Base.metadata,
                             Column('composite_discount_id', Integer, ForeignKey('CompositeDiscounts.discount_id')),
                             Column('discount_id', Integer, ForeignKey('discounts.discount_id'))
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
        'polymorphic_identity': 'CompositeDiscount'
    }

    def change_logic_operaor(self, lo):
        update('CompositeDiscounts').where(discount_id = self.discount_id).value(logic_operator = lo)
        session.commit()


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['CompositeDiscounts']], checkfirst=True)
        session.add(self)
        session.commit()

    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.CompositeDiscount import \
            CompositeDiscount
        compodis = CompositeDiscount(self.start_date, self.end_date, self.percent, self.min_amount, self.num_products_to_apply, self.store_id, self)
        compodis.set_id(self.discount_id)
        prods = {}
        for pidorm in self.products:
            prods[pidorm.product_name] = True
        compodis.products_in_discount = prods
        return compodis

    #TODO: check assosicaiton tables or change to assosication objects
    #TODO: go over all object constructors and make sure self.orm = orm is in else!!!!