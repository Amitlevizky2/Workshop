from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from project.data_access_layer import session,Base, engine
# from project.data_access_layer.RegisteredUserORM import RegisteredUserORM


class ManagerPermissionORM(Base):
    __tablename__ = 'managerpermissions'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    permission = Column(String, primary_key=True)


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['managerpermissions']], checkfirst=True)
        session.add(self)
        session.commit()

    def remove(self, username, store_id, permission):
        session.query(ManagerPermissionORM).delete.where(username=username, store_id=store_id, permission=permission)
