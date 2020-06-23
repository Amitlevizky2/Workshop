from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import session, Base, engine, proxy


class ManagerORM(Base):
    __tablename__ = 'managers'
    username = Column(String, ForeignKey('regusers.username'), primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    appointed_by = Column(String, ForeignKey('regusers.username'))
    manages = relationship("StoreORM", back_populates="managed_by")
    managed_by = relationship("RegisteredUserORM", back_populates="manages", foreign_keys=username)

    def add(self, manager):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
            proxy.get_session().add(manager)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error

    def remove(self):
        from project.data_access_layer.ManagerPermissionORM import ManagerPermissionORM
        res = proxy.get_session().query(ManagerPermissionORM).filter_by(username=self.username)
        for perm in res:
            proxy.get_session().delete(perm)
            proxy.get_session().commit()
        proxy.get_session().delete(self)
        proxy.get_session().commit()