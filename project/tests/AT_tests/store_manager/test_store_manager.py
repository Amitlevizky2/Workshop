import os
import unittest

from project.tests.AT_tests.store_owner.test_add_store_permiision_to_manager import AddStorePermission
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class StoreManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.service = Driver.make_bridge()
        self.service.register("new manager", "new pass")
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store")
        self.service.add_new_store_manager("new manager", self.store_id)
        self.service.add_permission(self.store_id, "new manager", "add_product")
        self.service.logout()
        self.service.login("new manager", "new pass")

    @classmethod
    def tearDownClass(cls):

        os.remove("C:\\Users\\Owner\\Desktop\\Sadna_project\\Workshop\\daldal.db")

    def test_manager_action_success(self):

        self.assertTrue(self.service.add_product_to_Store(self.store_id, *ATsetUP.products[0]))

    def test_manager_action_sad(self):
        res = self.service.add_new_store_manager("no permission", self.store_id)
        x=5
        self.assertTrue(res['error'])

    def test_manager_action_bad(self):
        self.service.logout()
        self.assertTrue(self.service.add_product_to_Store(self.store_id, *ATsetUP.products[0])['error'])
if __name__ == '__main__':
    unittest.main()
