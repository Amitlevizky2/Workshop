import unittest

from project.tests.AT_tests.store_owner.test_add_store_permiision_to_manager import AddStorePermission
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class StoreManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.register("new manager", "new pass")
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store")
        self.service.add_new_store_manager("new manager", self.store_id)
        self.service.add_permission(self.store_id, "new manager", "add_product")
        self.service.logout()
        self.service.login("new manager", "new pass")

    def test_manager_action_success(self):

        self.assertTrue(self.service.add_product_to_Store(self.store_id, *ATsetUP.products[0]))

    def test_manager_action_sad(self):
        self.assertFalse(self.service.add_new_store_manager("no permission", self.store_id))

    def test_manager_action_bad(self):
        self.service.logout()
        self.assertFalse(self.service.add_product_to_Store(self.store_id, *ATsetUP.products[0]))
if __name__ == '__main__':
    unittest.main()
