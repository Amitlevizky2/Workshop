from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy


def find_pass(username):
    return proxy.get_session().query(SecurityORM).filter_by(username=username).first()


class SecurityORM(Base):
    __tablename__ = 'passwords'
    username = Column(String, ForeignKey('regusers'), primary_key=True)
    hashed_pass = Column(String)

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['passwords']], checkfirst=True)
        proxy.get_session().add(self)
        proxy.get_session().commit()
