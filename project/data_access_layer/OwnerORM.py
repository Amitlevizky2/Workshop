from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy


class OwnerORM(Base):
    __tablename__ = 'owners'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    appointed_by = Column(String, ForeignKey('regusers.username'))
    store = relationship("StoreORM", back_populates="owned_by",foreign_keys=[store_id])
    user = relationship("RegisteredUserORM", back_populates="owns", foreign_keys=[username])

    def add(self, owner):
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        proxy.get_session().add(owner)
        proxy.get_session().commit()

    def remove(self):
        proxy.get_session().delete(self)
        proxy.get_session().commit()