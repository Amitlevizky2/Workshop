import os
from unittest import TestCase

from project.data_access_layer import *
from project.data_access_layer.ProductORM import ProductORM
from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer.BasketORM import BasketORM

from project.data_access_layer.OwnerORM import OwnerORM
from project.data_access_layer.ManagerORM import ManagerORM
from project.data_access_layer.StoreORM import StoreORM
from project.data_access_layer.PolicyORM import PolicyORM
from project.data_access_layer.VisibleProductDiscountORM import VisibleProductDiscountORM


class TestVisibleORM(TestCase):

    @classmethod
    def setUpClass(self) -> None:
        os.remove('C:\\Users\\Lielle Ravid\\Desktop\\sixth semster\\sadna\\version 1\\project\\tradeSystem.db')

    def setUp(self) -> None:
        self.store = StoreORM(id = 3456, name = "test_me", discount_idx = 0, purchases_idx = 0)
        self.store.add()
        self.product = ProductORM(name= "stuff", store_id= 3456, categories = "", key_words = "", price = 10, quantity = 5)
        self.orm = VisibleProductDiscountORM(discount_id = 1, store_id = 3456, start_date = None, end_date = None, percent = 40)
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['products']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['discounts']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['visibleProductDiscounts']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['Discount_products']], checkfirst=True)

    def test_add_success(self):
        num = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).count()
        self.orm.add()
        res = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).count()
        proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        self.assertEqual(num, res)

    def test_add_fail(self):
        self.orm.add()
        num = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).count()
        store = VisibleProductDiscountORM(discount_id = 1, store_id = 3456, start_date = None, end_date = None, percent = 40)
        res = store.add()
        self.assertEqual('<class \'sqlalchemy.orm.exc.FlushError\'>', res)
        proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).delete()
        proxy.get_session().commit()

    def test_update_success(self):
        self.orm.add()
        self.orm.percent=60
        res = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).first()
        self.assertTrue(res.percent is 60)

    def test_remove_success(self):
        proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        res = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id = 1).filter_by(store_id=3456).count()
        self.assertTrue(res == 0)

    def test_add_products_success(self):
        self.orm.add()
        num = proxy.get_session().query(ProductsInDiscountsORM).filter_by(discount_id = 1).filter_by(store_id=3456).count()
        self.orm.add_product("stuff")
        res = proxy.get_session().query(ProductsInDiscountsORM).filter_by(discount_id = 1).filter_by(store_id=3456).count()
        self.assertEqual(num + 1, res)
