import os
from datetime import datetime
from unittest import TestCase

from project.data_access_layer import *
from project.data_access_layer.ProductORM import ProductORM
from project.data_access_layer.PurchaseORM import PurchaseORM
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
        self.orm = RegisteredUserORM(username="Danny", admin=0)
        Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)
        self.orm.add()
        self.store = StoreORM(id = 3456, name = "test_me", discount_idx = 0, purchases_idx = 0)
        self.store.add()
        self.purchase = PurchaseORM(username= "Danny", store_id = 3456, date=datetime.today, id=4, order_number= 1000, supply_number =1000)
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['purchases']], checkfirst=True)

    def test_add_success(self):
        num = proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).count()
        self.purchase.add()
        res = proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).count()
        proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        self.assertEqual(num+1, res)

    def test_add_fail(self):
        self.purchase.add()
        num = proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).count()
        store = PurchaseORM(username= "Danny", store_id = 3456, date=datetime.today, id=4, order_number= 1000, supply_number =1000)
        res = store.add()
        self.assertEqual('<class \'sqlalchemy.orm.exc.FlushError\'>', res)
        proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).delete()
        proxy.get_session().commit()

    def test_update_success(self):
        self.purchase.add()
        self.purchase.set_order_number(3)
        res = proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).first()
        self.assertTrue(res.order_number is 3)

    def test_remove_success(self):
        proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).delete()
        proxy.get_session().commit()
        res = proxy.get_session().query(PurchaseORM).filter_by(username="Danny").filter_by(store_id=3456).count()
        self.assertTrue(res == 0)