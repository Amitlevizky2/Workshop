from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.DAL import Base


class RegisteredUserORM(Base):
    __tablename__ = 'regusers'
    username = Column(String, primary_key=True)
    hashed_pass = Column(String)
    #not sure if need back populate here
    baskets = relationship('BasketORM', back_populates="user")
    #not sure if needed
    cart_total = Column(Integer)
    #not sure if works