from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from project.data_access_layer import session
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM


class ManagerPermissionORM(RegisteredUserORM):
    __tablename__ = 'managerpermissions'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    permission = Column(String, primary_key=True)


    def add(self):
        session.add(self)

    def remove(self, username, store_id, permission):
        session.query(ManagerPermissionORM).delete.where(username=username, store_id=store_id, permission=permission)
