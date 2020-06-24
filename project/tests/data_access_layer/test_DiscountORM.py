


from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import relationship
from datetime import  datetime

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM




def find_by_id(discount_id):
    proxy.get_session().query(DiscountORM).filter_by(discount_id=discount_id).first()
def add( id, store_id):
    try:
        Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
        dis = DiscountORM(discount_id=id, store_id=store_id)
        proxy.get_session().add(dis)
        proxy.get_session().commit()

    except SQLAlchemyError as e:
        error = str(type(e))
        return error


class DiscountORM(Base):
    __tablename__ = 'discounts'
    discount_id = Column(Integer, primary_key=True)
    #maybenot needed?
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    #MODIFY TO STRING
    # start_date = Column(DateTime)
    # end_date = Column(DateTime)
    # percent = Column(Integer)
    products = relationship("ProductsInDiscountsORM")
    # discriminator = Column(String(50))
    #store = relationship("StoreORM", back_populates="discounts")
    # # __mapper_args__ = {
    #     'polymorphic_on': discriminator
    # }



    def update_precent(self, percent):
        self.percent = percent
        proxy.get_session().commit()

    def update_start(self, start):
        self.start_date = start
        proxy.get_session().commit()

    def update_end(self, end):
        self.end_date = end
        proxy.get_session().commit()

    def add_product(self, product_name):
        prod = ProductsInDiscountsORM(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id)
        prod.add()

    def remove_product(self, product_name):
        res= proxy.get_session().query(ProductsInDiscountsORM).filter_by(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id).first()
        proxy.get_session().delete(res)
        proxy.get_session().commit()

    def createObject(self):
        dis = None
        from project.data_access_layer.VisibleProductDiscountORM import VisibleProductDiscountORM
        res = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id=self.discount_id).filter_by(store_id=self.store_id).count()
        if res == 1:
            dis = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id=self.discount_id).filter_by(store_id=self.store_id).first()
        else:
            from project.data_access_layer.ConditionalProductDiscountORM import ConditionalProductDiscountsORM
            res = proxy.get_session().query(ConditionalProductDiscountsORM).filter_by(discount_id=self.discount_id).filter_by(store_id=self.store_id).count()
            if res == 1:
                dis = proxy.get_session().query(ConditionalProductDiscountsORM).filter_by(discount_id = self.discount_id).filter_by(store_id=self.store_id).first()
            else:
                from project.data_access_layer.ConditionalStoreDiscountORM import ConditionalStoreDiscountORM
                res = proxy.get_session().query(ConditionalStoreDiscountORM).filter_by(discount_id=self.discount_id).filter_by(store_id=self.store_id).count()
                if res == 1:
                    dis = proxy.get_session().query(ConditionalStoreDiscountORM).filter_by(discount_id =self.discount_id).filter_by(store_id=self.store_id).first()
                else:
                    from project.data_access_layer.CompositeDiscountORM import CompositeDiscountORM
                    res = proxy.get_session().query(CompositeDiscountORM).filter_by(discount_id=self.discount_id).filter_by(store_id=self.store_id).count()
                    if res == 1:
                        dis = proxy.get_session().query(CompositeDiscountORM).filter_by(
                            discount_id= self.discount_id).filter_by(store_id=self.store_id).first()
        return dis.createObject()
