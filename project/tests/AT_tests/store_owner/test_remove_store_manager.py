import unittest

from project.tests.AT_tests.test_env.Driver import Driver


class RemoveStoreManager(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.register("new manager", "new pass")
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store")
        self.service.add_new_store_manager("new manager", self.store_id)

    def test_remove_store_manager_success(self):
        self.assertFalse(self.service.remove_store_manager(self.store_id, "new manager"))
        self.service.logout()
        self.service.login("new manager", "new pass")
        self.assertNotIn(str(self.store_id), self.service.get_managed_stores())

    def test_remove_store_manager_sad(self):
        self.assertFalse(self.service.remove_store_manager(self.store_id, "not new manager"))
        self.service.logout()
        self.service.login("new manager", "new pass")
        self.assertFalse(self.service.remove_store_manager(str(self.store_id), "manager", ))

    def test_add_permission_bad(self):
        self.assertFalse(self.service.remove_store_manager(self.store_id + 40, "new manager"))
        self.service.logout()
        self.assertFalse(self.service.remove_store_manager(self.store_id, "new manager"))


if __name__ == '__main__':
    unittest.main()
