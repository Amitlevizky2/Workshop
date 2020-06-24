import datetime
from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, engine, proxy
from project.data_access_layer import DiscountORM


# class ConditionalStoreDiscountORM(DiscountORM):
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM


class ConditionalStoreDiscountORM(Base):
    __tablename__ = 'conditionalstorediscounts'
    # discount_id = id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    discount_id = Column(Integer, primary_key=True)
    min_price = Column(Integer)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    percent = Column(Integer)
    # # MODIFY TO STRING
    # __mapper_args__ = {
    #     'polymorphic_identity': 'ConditionalStore'
    # }

    def Update_min_price(self, min):
        self.min_price =min
        proxy.get_session().commit()

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
            Base.metadata.create_all(engine, [Base.metadata.tables['conditionalstorediscounts']], checkfirst=True)
            DiscountORM.add(self.discount_id, self.store_id)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(type(e))
            return error


    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalStoreDiscount import \
            ConditionalStoreDiscount
        condsdis = ConditionalStoreDiscount(self.start_date, self.end_date, (self.percent*100), self.min_price, self.store_id, self)
        condsdis.set_id(self.discount_id)
        prods = {}
        Base.metadata.create_all(engine, [Base.metadata.tables['Discount_products']], checkfirst=True)
        res = proxy.get_session().query(ProductsInDiscountsORM).filter(
            ProductsInDiscountsORM.discount_id == self.discount_id).filter(
            ProductsInDiscountsORM.store_id == self.store_id)
        for pidorm in res:
            prods[pidorm.product_name] = True
        condsdis.products_in_discount = prods
        return condsdis