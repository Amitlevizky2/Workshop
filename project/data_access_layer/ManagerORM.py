from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from project.data_access_layer import session,Base,engine



class ManagerORM(Base):
    __tablename__ = 'managers'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    appointed_by = Column(String, ForeignKey('regusers.username'))
    manages = relationship("StoreORM", back_populates="managed_by")
    managed_by = relationship("RegisteredUserORM", back_populates="manages", foreign_keys=username)

    def add(self, manager):
        Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
        session.add(manager)
        session.commit()

    def remove(self):
        session.delete(self)
        session.commit()