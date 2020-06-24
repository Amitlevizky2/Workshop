from sqlalchemy import Table, Column, Integer, ForeignKey, String, update, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from datetime import  datetime

from project.data_access_layer import Base, session, engine, proxy, DiscountORM

from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM



# class VisibleProductDiscountORM(DiscountORM):
class VisibleProductDiscountORM(Base):
    __tablename__ = 'visibleProductDiscounts'
    # discount_id = Column(Integer, ForeignKey("discounts.discount_id"), primary_key=True)
    discount_id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"), primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    percent = Column(Integer)
    # products = relationship("ProductsInDiscountsORM")
    # discriminator = Column(String(50))
    # parent = relationship("DiscountORM")
    # __mapper_args__ = {
    #     'polymorphic_identity': 'Visible Discount'
    # }

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
            Base.metadata.create_all(engine, [Base.metadata.tables['visibleProductDiscounts']], checkfirst=True)
            DiscountORM.add(self.discount_id, self.store_id)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            error = str(type(e))
            return error


    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import \
            VisibleProductDiscount
        visdis = VisibleProductDiscount(self.start_date, self.end_date, (self.percent*100), self.store_id, self)
        visdis.set_id(self.discount_id)
        prods = {}
        res = proxy.get_session().query(ProductsInDiscountsORM).filter(ProductsInDiscountsORM.discount_id==self.discount_id).filter(ProductsInDiscountsORM.store_id==self.store_id)
        for pidorm in res:
            prods[pidorm.product_name] = True
        visdis.products_in_discount = prods
        return visdis

    def add_product(self, product_name):
        prod = ProductsInDiscountsORM(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id)
        prod.add()

    def remove_product(self, product_name):
        res = proxy.get_session().query(ProductsInDiscountsORM).filter_by(discount_id=self.discount_id, product_name=product_name, store_id=self.store_id)
        proxy.get_session().delete(res)
        proxy.get_session().commmit()