from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session


association_managers = Table('managers', Base.metadata,
    Column('username', Integer, ForeignKey('regusers.username')),
    Column('store_id', Integer, ForeignKey('stores.id')),
    Column('appointed_by', String, ForeignKey('regusers.username'))
)

association_owners = Table('owners', Base.metadata,
    Column('username', Integer, ForeignKey('regusers.username')),
    Column('store_id', Integer, ForeignKey('stores.id')),
    Column('appointed_by', String, ForeignKey('regusers.username'))
)


def find_by_username(username):
    session.query(RegisteredUserORM).filter_by(username=username).first()



class RegisteredUserORM(Base):
    __tablename__ = 'regusers'
    username = Column(String, primary_key=True)
    #not sure if need back populate here
    baskets = relationship('BasketORM', back_populates="user")
    notifications = relationship('UserNotification', backpopulates='user')
    owns = relationship( "StoreORM", secondary=association_owners, back_populates="owned_by")
    manages = relationship("StoreORM", secondary=association_managers, back_populates="managed_by")
    ##OR THIS OR THIS
    owns = relationship("OwnerORM", back_populates="owned_by")
    manages = relationship("ManagerORM", back_populates="managed_by")


    def add(self):
        session.add(self)

    #what am i updating
    def update(self, username):
        session.query(RegisteredUserORM).filter_by(username=username).first().update()

