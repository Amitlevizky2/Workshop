from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.DAL import Base, session
from project.DAL.RegisteredUserORM import association_owners, association_managers


def find_store(store_id):
    return session.query(StoreORM).filter_by(store_id=store_id).first()



class StoreORM(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_index = Column(Integer)
    policy_index = Column(Integer)
    owned_by = relationship("RegisteredUserORM", secondary=association_owners, back_populates="owns")
    managed_by = relationship("RegisteredUserORM", secondary=association_managers, back_populates="manages")
    ## OR THIS OR THIS
    owned_by = relationship("OwnerORM", back_populates="owns")
    managed_by = relationship("ManagerORM", back_populates="manages")


