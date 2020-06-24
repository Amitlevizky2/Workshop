from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine, proxy


def add(id, store_id):
    try:
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        poli = PolicyORM(policy_id=id, store_id=store_id)
        proxy.get_session().add(poli)
        proxy.get_session().commit()
    except SQLAlchemyError as e:
        error = str(type(e))
        return error


class PolicyORM(Base):
    __tablename__ = 'policies'
    policy_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)

    def createObject(self):
        poli = None
        from project.data_access_layer.ProductPolciesORM import ProductPoliciesORM
        res = proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id=self.policy_id).filter_by(store_id=self.store_id).count()
        if res == 1:
            from project.data_access_layer.ProductPolciesORM import ProductPoliciesORM
            poli = proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id=self.policy_id).filter_by(store_id=self.store_id).first()
        else:
            from project.data_access_layer.StorePolicyORM import StorePolicyORM
            res = proxy.get_session().query(StorePolicyORM).filter_by(policy_id=self.policy_id).filter_by(store_id=self.store_id).count()
            if res == 1:
                poli = proxy.get_session().query(StorePolicyORM).filter_by(policy_id=self.policy_id).filter_by(store_id=self.store_id).first()
            else:
                from project.data_access_layer.CompositePolicyORM import CompositePolicyORM
                res = proxy.get_session().query(CompositePolicyORM).filter_by(policy_id=self.policy_id).filter_by(store_id=self.store_id).count()
                if res == 1:
                    poli = proxy.get_session().query(CompositePolicyORM).filter_by(policy_id=self.policy_id).filter_by(store_id=self.store_id).first()
        return poli.createObject()