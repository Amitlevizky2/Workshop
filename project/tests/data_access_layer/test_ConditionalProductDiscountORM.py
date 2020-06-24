import datetime


from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, engine, session, proxy
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer import DiscountORM



# class ConditionalProductDiscountsORM(DiscountORM):
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM


class ConditionalProductDiscountsORM(Base):
    __tablename__ = 'conditionalproductdiscounts'
    # discount_id = Column(Integer, ForeignKey('discounts.discount_id'), primary_key=True)
    discount_id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    percent = Column(Integer)
    min_amount = Column(Integer)
    num_products_to_apply = Column(Integer)
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    # MODIFY TO STRING
    # __mapper_args__ = {
    #     'polymorphic_identity': 'ConditionalProduct'
    # }

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
            Base.metadata.create_all(engine, [Base.metadata.tables['conditionalproductdiscounts']], checkfirst=True)
            DiscountORM.add(self.discount_id, self.store_id)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(type(e))
            return error


    def update_min_amount(self, min):
        self.min_amount = min
        proxy.get_session().commit()

    def update_num_to_apply(self, num):
        self.num_products_to_apply = num
        proxy.get_session().commit()

    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalProductDiscount import \
            ConditionalProductDiscount
        condpdis = ConditionalProductDiscount(self.start_date, self.end_date, (self.percent*100), self.min_amount, self.num_products_to_apply, self.store_id, self)
        condpdis.set_id(self.discount_id)
        prods = {}
        res = proxy.get_session().query(ProductsInDiscountsORM).filter(
            ProductsInDiscountsORM.discount_id == self.discount_id).filter(
            ProductsInDiscountsORM.store_id == self.store_id)
        for pidorm in res:
            prods[pidorm.product_name] = True
        condpdis.products_in_discount = prods
        return condpdis

    def add_product(self, product_name):
        from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM
        prod = ProductsInDiscountsORM(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id)
        prod.add()

    def remove_product(self, product_name):
        res = proxy.get_session().query(ProductsInDiscountsORM).filter_by(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id).first()
        proxy.get_session().delete(res)
        proxy.get_session().commit()