from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session,engine

#from project.data_access_layer.OwnerORM import OwnerORM



def find_by_username(username):
    return session.query(RegisteredUserORM).filter_by(username=username).first()



class RegisteredUserORM(Base):
    from project.data_access_layer.UserNotificationsORM import UserNotificationORM

    from project.data_access_layer.StoreORM import StoreORM
    __tablename__ = 'regusers'
    username = Column(String, primary_key=True)
    baskets = relationship('BasketORM', back_populates="user")
    notifications = relationship('UserNotificationORM')

    owns = relationship('OwnerORM', back_populates="user",foreign_keys="OwnerORM.username")
    manages = relationship("ManagerORM", back_populates="managed_by",foreign_keys="ManagerORM.username")

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)
        session.add(self)
        session.commit()

    def add_notification(self, username, message):
        from project.data_access_layer.UserNotificationsORM import UserNotificationORM
        notif = UserNotificationORM(username=username, notification=message)
        session.add(notif)
        session.commit()
