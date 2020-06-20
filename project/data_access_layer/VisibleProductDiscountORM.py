from sqlalchemy import Table, Column, Integer, ForeignKey, String,update
from sqlalchemy.orm import relationship
from datetime import  datetime

from project.data_access_layer import Base, session, engine
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM



class VisibleProductDiscountORM(DiscountORM):
    __tablename__ = 'visibleProductDiscounts'
    discount_id = Column(Integer, ForeignKey("discounts.discount_id"), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'Visible Discount'
    }

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['visibleProductDiscounts']], checkfirst=True)
        session.add(self)
        session.commit()

    def createObject(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import \
            VisibleProductDiscount
        visdis = VisibleProductDiscount(self.start_date, self.end_date, self.percent, self.store_id, self)
        visdis.set_id(self.discount_id)
        prods = {}
        for pidorm in self.products:
            prods[pidorm.product_name] = True
        visdis.products_in_discount = prods
        return visdis
