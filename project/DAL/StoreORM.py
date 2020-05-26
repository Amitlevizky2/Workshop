from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.DAL import Base


class StoreORM(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_index = Column(Integer)
    policy_index = Column(Integer)
    managers = relationship('ManagerORM', back_populates="store")
    owners = relationship('OwnerORM', back_populates="store")