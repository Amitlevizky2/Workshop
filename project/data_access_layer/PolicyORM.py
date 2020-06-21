from sqlalchemy import Table, Column, Integer, ForeignKey, String, update
from sqlalchemy.orm import relationship

from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer import Base, session, engine


class PolicyORM(Base):
    __tablename__ = 'policies'
    policy_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    discriminator = Column('type', String(50))
    products = relationship("ProductsInPoliciesORM")
    __mapper_args__ = {
        'polymorphic_identity': 'policy',
        'polymorphic_on': discriminator
    }
    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        session.add(self)
        session.commit()