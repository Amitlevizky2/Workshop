import unittest

from project.data_access_layer import Base, engine
from project.domain_layer.users_managment.UsersManager import UsersManager
from project.tests.AT_tests.test_env.Driver import Driver


class RemoveStoreManager(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.real.store_manager_interface.stores_manager.users_manager = UsersManager(None)
        self.service.register("new manager", "new pass")
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store")
        self.service.add_new_store_manager("new manager", self.store_id)

    def test_remove_store_manager_success(self):
        res0= self.service.remove_store_manager(self.store_id, "new manager")
        x=5
        self.assertTrue(res0)
        self.service.logout()
        self.service.login("new manager", "new pass")
        self.assertNotIn(self.store_id, self.service.get_managed_stores())

    def test_remove_store_manager_sad(self):
        self.assertTrue(self.service.remove_store_manager(self.store_id, "not new manager"))
        self.service.logout()
        self.service.login("new manager", "new pass")
        self.assertTrue(self.service.remove_store_manager(self.store_id, "manager", ))

    def test_add_permission_bad(self):
        self.assertTrue(self.service.remove_store_manager(self.store_id + 40, "new manager"))
        self.service.logout()
        self.assertTrue(self.service.remove_store_manager(self.store_id, "new manager"))


    def tearDown(self) -> None:
        self.drop_table('stores')
        self.drop_table('baskets')
        self.drop_table('CompositeDiscounts')
        self.drop_table('CompositePolicies')
        self.drop_table('conditionalproductdiscounts')
        self.drop_table('conditionalstorediscounts')
        self.drop_table('discounts')
        self.drop_table('to_apply_composite')
        self.drop_table('managers')
        self.drop_table('managerpermissions')
        self.drop_table('owners')
        self.drop_table('Policy_in_composite')
        self.drop_table('policies')
        self.drop_table('predicates')
        self.drop_table('products')
        self.drop_table('productspolicies')
        self.drop_table('productsinbaskets')
        self.drop_table('Discount_products')
        self.drop_table('Policy_products')
        self.drop_table('productsinpurcases')
        self.drop_table('purchases')
        self.drop_table('regusers')
        self.drop_table('stores')
        self.drop_table('storepolicies')
        self.drop_table('passwords')
        self.drop_table('notifications')
        self.drop_table('visibleProductDiscounts')
        # self.drop_table('stores')

    def drop_table(self, table_name: str):
        if table_name in Base.metadata.tables:
            Base.metadata.drop_all(engine, [Base.metadata.tables[table_name]])

if __name__ == '__main__':
    unittest.main()
