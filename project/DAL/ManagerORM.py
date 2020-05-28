from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from project.DAL import session
from project.DAL.RegisteredUserORM import RegisteredUserORM


class ManagerORM(RegisteredUserORM):
    __tablename__ = 'owners'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    appointed_by = Column(String, ForeignKey('regusers.username'))
    manages = relationship("StoreORM", back_populates="managed_by")
    managed_by = relationship("RegUserORM", back_populates="manages")

    def add(self, manager):
        session.add(manager)