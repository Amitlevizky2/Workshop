from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.DiscountToApplyORM import DiscountToApplyORM
from project.data_access_layer.PredicateORM import PredicateORM
from project.data_access_layer import DiscountORM


from project.data_access_layer import Base, session, engine, proxy
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator


def find_by_id(discount_id):
    proxy.get_session().query(DiscountORM).filter_by(discount_id=discount_id).first()


# class CompositeDiscountORM(DiscountORM):
class CompositeDiscountORM(Base):
    __tablename__ = 'CompositeDiscounts'
    # discount_id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    discount_id = Column(Integer, primary_key=True)
    logic_operator = Column(String)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    percent = Column(Integer)
    # MODIFY TO STRING
    products_in_predicates = relationship("PredicateORM")
    discounts_to_apply = relationship("DiscountToApplyORM")
    # __mapper_args__ = {
    #     'polymorphic_identity': 'CompositeDiscount'
    # }

    def change_logic_operaor(self, lo):
        self.logic_operator = lo
        proxy.get_session().commit()


    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
            Base.metadata.create_all(engine, [Base.metadata.tables['CompositeDiscounts']], checkfirst=True)
            DiscountORM.add(self.discount_id, self.store_id)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(type(e))
            return error

    def get_logic_operator(self, logic_operator_str:str):
        if logic_operator_str is None:
            return None
        if logic_operator_str.upper() == "LogicOperator.OR":
            return LogicOperator.OR
        elif logic_operator_str.upper() == "LogicOperator.AND":
            return LogicOperator.AND
        elif logic_operator_str.upper() == "LogicOperator.XOR":
            return LogicOperator.XOR
        else:
            return None

    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.CompositeDiscount import \
            CompositeDiscount
        to_apply =[]
        for dis in self.discounts_to_apply:
            real = dis.discount.createObject()
            to_apply.append(to_apply)
        pred = []
        pred_map_discount={}
        pred_map_prods={}
        res = proxy.get_session().query(PredicateORM).filter(PredicateORM.composite_discount_id==self.discount_id).filter(PredicateORM.store_id==self.store_id)
        for pre in res:
            from project.data_access_layer.DiscountORM import DiscountORM
            discount = proxy.get_session().query(DiscountORM).filter(DiscountORM.discount_id==pre.discount_id).filter(DiscountORM.store_id==pre.store_id).first()
            real_discount = discount.createObject()
            if real_discount.id not in pred_map_discount.keys():
                pred_map_discount[real_discount.id] = real_discount
                pred_map_prods[real_discount.id] = []
            pred_map_prods[real_discount.id].append(pre.product_name)
        for dis_id in pred_map_discount.keys():
            pred.append((pred_map_discount[dis_id], pred_map_prods[dis_id]))

        compodis = CompositeDiscount(self.start_date, self.end_date, self.get_logic_operator(self.logic_operator), pred, to_apply, self.store_id, self)
        compodis.set_id(self.discount_id)
        return compodis

    #TODO: check assosicaiton tables or change to assosication objects
    #TODO: go over all object constructors and make sure self.orm = orm is in else!!!!