from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy


def find_all_notifications(username):
    return proxy.get_session().query(UserNotificationORM).filter_by(username=username)



class UserNotificationORM(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('regusers.username'))
    notification = Column(String)
    # user = relationship("RegisteredUserORM", back_populates="notifications")
    #Base.metadata.create_all(engine)

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['notifications']], checkfirst=True)
        proxy.get_session().add(self)
        proxy.get_session().commit()