from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from project.DAL import Base, session


class OwnerORM(Base):
    __tablename__ = 'owners'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    appointed_by = Column(String, ForeignKey('regusers.username'))
    owns = relationship("StoreORM", back_populates="owned_by")
    owned_by = relationship("RegUserORM", back_populates="owns")


    def add(self, owner):
        session.add(owner)
