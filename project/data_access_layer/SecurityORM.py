from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session



def find_pass(username):
    return session.query(SecurityORM).filter_by(username=username).first()



class SecurityORM(Base):
    __tablename__ = 'passwords'
    username = Column(String, ForeignKey('regusers'), primary_key=True)
    hashed_pass = Column(String)