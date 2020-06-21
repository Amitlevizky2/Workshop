import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.DiscountORM import DiscountORM

class ConditionalStoreDiscountORM(DiscountORM):
    __tablename__ = 'conditionalstorediscounts'
    discount_id = id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    min_price = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'ConditionalStore',
    }

    def Update_min_price(self, min):
        self.min_price =min
        session.commit()

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['conditionalstorediscounts']], checkfirst=True)
        session.add(self)
        session.commit()

    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalStoreDiscount import \
            ConditionalStoreDiscount
        condsdis = ConditionalStoreDiscount(self.start_date, self.end_date, self.percent, self.min_price, self.store_id, self)
        condsdis.set_id(self.discount_id)
        prods = {}
        for pidorm in self.products:
            prods[pidorm.product_name] = True
        condsdis.products_in_discount = prods
        return condsdis