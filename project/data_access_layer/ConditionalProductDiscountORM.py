import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, engine, session
from project.data_access_layer.DiscountORM import DiscountORM



class ConditionalProductDiscountsORM(DiscountORM):
    __tablename__ = 'conditionalproductdiscounts'
    discount_id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    min_amount = Column(Integer)
    num_products_to_apply = Column(Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'ConditionalProduct'
    }

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['conditionalproductdiscounts']], checkfirst=True)
        session.add(self)
        session.commit()

    def update_min_amount(self, min):
        update('conditionalproductdiscounts').where(discount_id=self.discount_id).values(min_amount=min)
        session.commit()

    def update_num_to_apply(self, num):
        update('conditionalproductdiscounts').where(discount_id=self.discount_id).values(num_products_to_apply=num)
        session.commit()

    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalProductDiscount import \
            ConditionalProductDiscount
        condpdis = ConditionalProductDiscount(self.start_date, self.end_date, self.percent, self.min_amount, self.num_products_to_apply, self.store_id, self)
        condpdis.set_id(self.discount_id)
        prods = {}
        for pidorm in self.products:
            prods[pidorm.product_name] = True
        condpdis.products_in_discount = prods
        return condpdis