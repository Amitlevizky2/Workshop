from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.DiscountToApplyORM import DiscountToApplyORM
from project.data_access_layer.PredicateORM import PredicateORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM


from project.data_access_layer import Base, session, engine






def find_by_id(discount_id):
    session.query(DiscountORM).filter_by(discount_id=discount_id).first()


class CompositeDiscountORM(DiscountORM):
    __tablename__ = 'CompositeDiscounts'
    discount_id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    logic_operator = Column(String)
    products_in_predicates = relationship("PredicateORM")
    discounts_to_apply = relationship("DiscountToApplyORM")
    __mapper_args__ = {
        'polymorphic_identity': 'CompositeDiscount'
    }

    def change_logic_operaor(self, lo):
        self.logic_operator = lo
        session.commit()


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['CompositeDiscounts']], checkfirst=True)
        session.add(self)
        session.commit()

    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.CompositeDiscount import \
            CompositeDiscount
        to_apply =[]
        for dis in self.discounts_to_apply:
            real = dis.createObject()
            to_apply.append(to_apply)
        pred = []
        pred_map_discount={}
        pred_map_prods={}
        for pre in self.products_in_predicates:
            real_discount = pre.discount.createObject()
            if real_discount.discount_id not in pred_map_discount.keys():
                pred_map_discount[real_discount.discount_id] = real_discount
            pred_map_prods[real_discount.discount_id].append(pre.product_name)
        for dis_id in pred_map_discount.keys():
            pred.append((pred_map_discount[dis_id], pred_map_prods[dis_id]))
        compodis = CompositeDiscount(self.start_date, self.end_date, self.logic_operator, pred, to_apply, self.store_id, self)
        compodis.set_id(self.discount_id)
        return compodis

    #TODO: check assosicaiton tables or change to assosication objects
    #TODO: go over all object constructors and make sure self.orm = orm is in else!!!!