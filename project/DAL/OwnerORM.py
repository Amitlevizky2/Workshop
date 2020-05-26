from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from project.DAL import Base


class OwnerORM(Base):
    __tablename__ = 'managers'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    appointed_by = Column(String, ForeignKey('regusers.username'))
    store = relationship('StoreORM', back_populates="owners")