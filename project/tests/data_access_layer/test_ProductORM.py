import os
from unittest import TestCase

from project.data_access_layer import *
from project.data_access_layer.ProductORM import ProductORM
from project.data_access_layer.RegisteredUserORM import RegisteredUserORM

from project.data_access_layer.BasketORM import BasketORM

from project.data_access_layer.OwnerORM import OwnerORM
from project.data_access_layer.ManagerORM import ManagerORM
from project.data_access_layer.StoreORM import StoreORM
from project.data_access_layer.PolicyORM import PolicyORM


class TestStoreORM(TestCase):

    @classmethod
    def setUpClass(self) -> None:
        os.remove('C:\\Users\\Lielle Ravid\\Desktop\\sixth semster\\sadna\\version 1\\project\\tradeSystem.db')

    def setUp(self) -> None:
        self.store = StoreORM(id = 3456, name = "test_me", discount_idx = 0, purchases_idx = 0)
        self.store.add()
        self.orm = ProductORM(name= "stuff", store_id= 3456, categories = "", key_words = "", price = 10, quantity = 5)
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['products']], checkfirst=True)

    def test_add_success(self):
        num = proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).count()
        self.orm.add()
        res = proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).count()
        proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        self.assertEqual(num+1, res)

    def test_add_fail(self):
        self.orm.add()
        num = proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).count()
        store = ProductORM(name= "stuff", store_id= 3456, categories = "", key_words = "", price = 10, quantity = 5)
        res = store.add()
        self.assertEqual('<class \'sqlalchemy.orm.exc.FlushError\'>', res)
        proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).delete()
        proxy.get_session().commit()

    def test_update_success(self):
        self.orm.add()
        self.orm.update_product_amount(3)
        res = proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).first()
        self.assertTrue(res.quantity is 3)

    def test_remove_success(self):
        proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        res = proxy.get_session().query(ProductORM).filter_by(name="stuff").filter_by(store_id=3456).count()
        self.assertTrue(res == 0)
