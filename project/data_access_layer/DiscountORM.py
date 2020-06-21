from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, DateTime
from sqlalchemy.orm import relationship
from datetime import  datetime

from project.data_access_layer import Base, session, engine
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM


def find_by_id(discount_id):
    session.query(DiscountORM).filter_by(discount_id=discount_id).first()


class DiscountORM(Base):
    __tablename__ = 'discounts'
    discount_id = Column(Integer, primary_key=True)
    #maybenot needed?
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    #MODIFY TO STRING
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    percent = Column(Integer)
    products = relationship("ProductsInDiscountsORM")
    discriminator = Column('type', String(50))
    #store = relationship("StoreORM", back_populates="discounts")
    __mapper_args__ = {
        'polymorphic_identity': 'discount',
        'polymorphic_on': discriminator
    }

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
        session.add(self)
        session.commit()


    def update_precent(self, percent):
        self.percent = percent
        session.commit()

    def update_start(self, start):
        self.start_date = start
        session.commit()

    def update_end(self, end):
        self.end_date = end
        session.commit()

    def add_product(self, product_name):
        prod = ProductsInDiscountsORM(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id)
        prod.add()

    def remove_product(self, product_name):
        session.query(ProductsInDiscountsORM).delete.where(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id)
