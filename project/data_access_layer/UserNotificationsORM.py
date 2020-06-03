from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session



def find_all_notifications(username):
    return session.query(UserNotificationORM).filter_by(username=username)



class UserNotificationORM(Base):
    __tablename__ = 'notifications'
    username = Column(String, ForeignKey('regusers'), primary_key=True)
    notification = Column(String)

    def add(self):
        session.add(self)