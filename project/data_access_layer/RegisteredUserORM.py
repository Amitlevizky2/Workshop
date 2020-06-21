from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, exc
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
    owns = relationship('OwnerORM', foreign_keys="OwnerORM.username")
    manages = relationship("ManagerORM", foreign_keys="ManagerORM.username")


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)
        try:
            session.add(self)
            session.commit()
        except exc.SQLAlchemyError:
            pass
            #try catch what do i do with catch


    def add_notification(self, username, message):
        from project.data_access_layer.UserNotificationsORM import UserNotificationORM
        notif = UserNotificationORM(username=username, notification=message)
        session.add(notif)
        session.commit()

    def createObject(self):
        from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
        user = RegisteredUser(self.username, self)
        managed_stores = []
        for owner in self.owns:
            managed_stores.append(owner.store_id)
        for manager in self.manages:
            managed_stores.append(manager.store_id)
        user.managed_stores = managed_stores
        notifies =[]
        for noti in self.notifications:
            notifies.append(noti.notification)
        user.notifications = notifies
        basks = {}
        for basket in self.baskets:
            basks[basket.store_id] = basket.createObject()
        user.cart.baskets = basks
        ##ADD PURCHASE LIST?
        return user