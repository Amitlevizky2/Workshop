import unittest

from project.tests.AT_tests.test_env.Driver import Driver


class AddStorePermission(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.register("new manager", "new pass")
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store")
        self.service.add_new_store_manager("new manager", self.store_id)

    def test_add_permission_success(self):
        self.assertTrue(self.service.add_permission(self.store_id, "new manager", "add_product"))
        self.service.logout()
        self.service.login("new manager", "new pass")
        self.assertTrue(self.service.add_product_to_Store(self.store_id, "iphone", 5, ["phones"], ["electronics"], 2))

    def test_add_permission_sad(self):

        self.assertTrue(self.service.add_permission(self.store_id, "not new manager", "add_product")['error'])
        self.service.logout()
        self.service.login("new manager", "new pass")
        self.assertTrue(self.service.add_permission(self.store_id, "manager", "add_product")['error'])

    def test_add_permission_bad(self):
        self.assertFalse(not self.service.add_permission(self.store_id+40, "new manager", "add_product")['error'])
        self.service.logout()
        self.assertFalse(not self.service.add_permission(self.store_id, "new manager", "add_product")['error'])


if __name__ == '__main__':
    unittest.main()
