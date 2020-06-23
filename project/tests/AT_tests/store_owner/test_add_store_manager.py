import unittest

from project.tests.AT_tests.test_env.Driver import Driver


class test_addStoremanager(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.register("new manager", "new pass")
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store") 

    def test_add_new_manager_success(self):
        self.assertTrue(self.service.add_new_store_manager("new manager", self.store_id))
        self.service.logout()
        self.service.login("new manager", "new pass")
        maneged_stores = self.service.get_managed_stores()
        self.assertIn(self.store_id,maneged_stores)

    def test_add_new_manager_sad(self):
        self.assertTrue(self.service.add_new_store_manager("not new manager", self.store_id)['error'])
        self.test_add_new_manager_success()
        self.service.logout()
        self.service.login("owner", "pass")
        self.assertTrue(self.service.add_new_store_manager("new manager", self.store_id)['error'])

    def test_add_new_manager_bad(self):
        self.assertTrue(self.service.add_new_store_manager("not new manager", self.store_id+40))
        x=5

if __name__ == '__main__':
    unittest.main()
