import os
from unittest import TestCase

from project.data_access_layer import *
from project.data_access_layer.ProductORM import ProductORM
from project.data_access_layer.ProductPolciesORM import ProductPoliciesORM
from project.data_access_layer.ProductsInPoliciesORM import ProductsInPoliciesORM
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
        self.orm = ProductPoliciesORM(policy_id = 1, store_id = 3456, min_amount = 5, max_amount = 13)
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['products']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['productspolicies']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['Policy_products']], checkfirst=True)

    def test_add_success(self):
        num = proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).count()
        self.orm.add()
        res = proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).count()
        proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        self.assertEqual(num+1, res)

    def test_add_fail(self):
        self.orm.add()
        num = proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).count()
        store = ProductPoliciesORM(policy_id = 1, store_id = 3456, min_amount = 5, max_amount = 13)
        res = store.add()
        self.assertEqual('<class \'sqlalchemy.orm.exc.FlushError\'>', res)
        proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).delete()
        proxy.get_session().commit()

    def test_update_success(self):
        self.orm.add()
        self.orm.max_amount=60
        res = proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).first()
        self.assertTrue(res.max_amount is 60)

    def test_remove_success(self):
        proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        res = proxy.get_session().query(ProductPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).count()
        self.assertTrue(res == 0)

    def test_add_products_success(self):
        self.orm.add()
        num = proxy.get_session().query(ProductsInPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).count()
        self.orm.add_product("stuff")
        res = proxy.get_session().query(ProductsInPoliciesORM).filter_by(policy_id = 1).filter_by(store_id=3456).count()
        self.assertEqual(num + 1, res)


