import os
from unittest import TestCase

from project.data_access_layer import *
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
        self.orm = StoreORM(id = 3456, name = "test_me", discount_idx = 0, purchases_idx = 0)
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)

    def test_add_success(self):
        num = proxy.get_session().query(StoreORM).filter_by(id=3456).count()
        self.orm.add()
        res = proxy.get_session().query(StoreORM).filter_by(id=3456).count()
        proxy.get_session().query(StoreORM).filter_by(id=3456).delete()
        proxy.get_session().commit()
        self.assertEqual(num+1, res)

    def test_add_fail(self):
        self.orm.add()
        num = proxy.get_session().query(StoreORM).filter_by(id=3456).count()
        store = StoreORM(id = 3456, name = "test_me", discount_idx = 0, purchases_idx = 0)
        res = store.add()
        self.assertEqual('<class \'sqlalchemy.orm.exc.FlushError\'>', res)
        proxy.get_session().query(StoreORM).filter_by(id=3456).delete()
        proxy.get_session().commit()

    def test_update_success(self):
        self.orm.add()
        self.orm.discount_idx =20
        proxy.get_session().commit()
        res = proxy.get_session().query(StoreORM).filter_by(id=3456).first()
        self.assertTrue(res.discount_idx is 20)

    def test_remove_success(self):
        proxy.get_session().query(StoreORM).filter_by(id=3456).delete()
        proxy.get_session().commit()
        res = proxy.get_session().query(StoreORM).filter_by(id=3456).count()
        self.assertTrue(res == 0)
