from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship
from datetime import datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.PolicyORM import PolicyORM
from project.data_access_layer.PoliciesInCompositeORM import PoliciesInCompositeORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine, proxy


class CompositePolicyORM(PolicyORM):
    __tablename__ = 'CompositePolicies'
    policy_id = Column(Integer, ForeignKey('policies.policy_id'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    logic_operator = Column(Integer)
    policies_to_apply = relationship("PoliciesInCompositeORM")
    __mapper_args__ = {
        'polymorphic_identity': 'Composite Policy'
    }

    def change_logic_operaor(self, lo):
        self.logic_operator = lo
        proxy.get_session().commit()

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['CompositePolicies']], checkfirst=True)
        proxy.get_session().add(self)
        proxy.get_session().commit()

    def add_policies(self, purchase_policies):
        for policy in purchase_policies:
            self.add_policy(policy)

    def add_policy(self, policy):
        from project.data_access_layer.PoliciesInCompositeORM import PoliciesInCompositeORM
        poliorm = PoliciesInCompositeORM(composite_discount_id=self.policy_id, policy_id=policy.id,
                                         store_id=self.store_id)
        poliorm.add()

    def remove_policy(self, policy):
        proxy.get_session().query(PoliciesInCompositeORM).delete.where(composite_discount_id=self.policy_id, policy_id=policy.id,
                                         store_id=self.store_id)

    def createObject(self):
        #CHANGEEEEEEE
        from project.domain_layer.stores_managment.DiscountsPolicies.CompositeDiscount import \
            CompositeDiscount
        to_apply = []
        for dis in self.discounts_to_apply:
            real = dis.createObject()
            to_apply.append(to_apply)
        pred = []
        pred_map_discount = {}
        pred_map_prods = {}
        for pre in self.products_in_predicates:
            real_discount = pre.discount.createObject()
            if real_discount.discount_id not in pred_map_discount.keys():
                pred_map_discount[real_discount.discount_id] = real_discount
            pred_map_prods[real_discount.discount_id].append(pre.product_name)
        for dis_id in pred_map_discount.keys():
            pred.append((pred_map_discount[dis_id], pred_map_prods[dis_id]))
        compodis = CompositeDiscount(self.start_date, self.end_date, self.logic_operator, pred, to_apply, self.store_id,
                                     self)
        compodis.set_id(self.discount_id)
        return compodis
