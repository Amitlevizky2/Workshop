from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, exc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy


#from project.data_access_layer.OwnerORM import OwnerORM
from project.data_access_layer.PurchaseORM import PurchaseORM


def find_by_username(username):
    return proxy.get_session().query(RegisteredUserORM).filter_by(username=username).first()



class RegisteredUserORM(Base):
    from project.data_access_layer.UserNotificationsORM import UserNotificationORM
    __tablename__ = 'regusers'
    username = Column(String, primary_key=True)
    admin = Column(Integer)
    baskets = relationship('BasketORM', back_populates="user")
    notifications = relationship('UserNotificationORM')
    owns = relationship('OwnerORM', foreign_keys="OwnerORM.username")
    manages = relationship("ManagerORM", foreign_keys="ManagerORM.username")

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(type(e))
            #print(error)
            return error

    def make_admin(self):
        self.admin = 1
        proxy.get_session().commit()

    def add_notification(self, username, message):
        from project.data_access_layer.UserNotificationsORM import UserNotificationORM
        notif = UserNotificationORM(username=username, notification=message)
        proxy.get_session().add(notif)
        proxy.get_session().commit()

    def createObject(self):
        from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
        user = RegisteredUser(self.username, self)
        managed_stores = []
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        for owner in self.owns:
            managed_stores.append(owner.store_id)
        Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
        for manager in self.manages:
            managed_stores.append(manager.store_id)
        user.managed_stores = managed_stores
        notifies =[]
        Base.metadata.create_all(engine, [Base.metadata.tables['notifications']], checkfirst=True)
        for noti in self.notifications:
            notifies.append(noti.notification)
        user.notifications = notifies
        basks = {}
        Base.metadata.create_all(engine, [Base.metadata.tables['baskets']], checkfirst=True)
        for basket in self.baskets:
            basks[basket.store_id] = basket.createObject()
        user.cart.baskets = basks
        if self.admin is 1:
            user.is_admin = True
        Base.metadata.create_all(engine, [Base.metadata.tables['purchases']], checkfirst=True)
        orms = proxy.get_handler_session().query(PurchaseORM).filter_by(username=self.username)
        purchases = []
        for p in orms:
            purchase = p.createObject()
            purchases.append(purchase)
        user.purchase_history = purchases
        return user