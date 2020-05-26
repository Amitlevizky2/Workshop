from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from project.DAL.RegisteredUserORM import RegisteredUserORM


class ManagerPermissionORM(RegisteredUserORM):
    __tablename__ = 'managerpermissions'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    permission = Column(Integer, primary_key=True)
