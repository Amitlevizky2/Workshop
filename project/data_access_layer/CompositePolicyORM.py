from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer import PolicyORM
from project.data_access_layer.PoliciesInCompositeORM import PoliciesInCompositeORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine, proxy
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator


class CompositePolicyORM(Base):
    __tablename__ = 'CompositePolicies'
    policy_id = Column(Integer, ForeignKey('policies.policy_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    logic_operator = Column(Integer)
    policies_to_apply = relationship("PoliciesInCompositeORM")

    def change_logic_operaor(self, lo):
        self.logic_operator = lo
        proxy.get_session().commit()

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['CompositePolicies']], checkfirst=True)
            PolicyORM.add(self.policy_id, self.store_id)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(type(e))
            return error


    def add_policies(self, purchase_policies):
        for policy in purchase_policies:
            self.add_policy(policy)

    def add_policy(self, policy):
        from project.data_access_layer.PoliciesInCompositeORM import PoliciesInCompositeORM
        poliorm = PoliciesInCompositeORM(composite_discount_id=self.policy_id, policy_id=policy.id,
                                         store_id=self.store_id)
        poliorm.add()

    def remove_policy(self, policy):
        proxy.get_session().query(PoliciesInCompositeORM).filter_by(composite_discount_id=self.policy_id, policy_id=policy.id,
                                         store_id=self.store_id).first()

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
        from project.domain_layer.stores_managment.PurchasesPolicies.PurchaseCompositePolicy import \
            PurchaseCompositePolicy
        to_apply = []
        Base.metadata.create_all(engine, [Base.metadata.tables['Policy_in_composite']], checkfirst=True)
        res = proxy.get_session().query(PoliciesInCompositeORM).filter(PoliciesInCompositeORM.policy_id==self.policy_id).filter(PoliciesInCompositeORM.store_id==self.store_id)
        for poli in res:
            pol = poli.createObject()
            to_apply.append(pol)
        compopol = PurchaseCompositePolicy(to_apply, self.get_logic_operator(self.logic_operator), self.policy_id, self.store_id, self)
        return compopol
