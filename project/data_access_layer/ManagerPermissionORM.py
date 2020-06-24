from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import session,Base, engine,proxy
# from project.data_access_layer.RegisteredUserORM import RegisteredUserORM


class ManagerPermissionORM(Base):
    __tablename__ = 'managerpermissions'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    permission = Column(String, primary_key=True)


    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['managerpermissions']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(type(e))
            return error


    def remove(self, username, store_id, permission):
        res = proxy.get_session().query(ManagerPermissionORM).filter(username=username, store_id=store_id, permission=permission).first()
        proxy.get_session().delete(res)
        proxy.get_session().commit()
