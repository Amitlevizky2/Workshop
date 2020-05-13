import unittest

from project.tests.AT_tests.test_env.Driver import Driver


class addStoreOwner(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.register("new owner", "new pass")
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store")

    def test_add_new_owner_success(self):
        self.assertTrue(self.service.add_new_store_owner("new owner", self.store_id))
        self.service.logout()
        self.service.login("new owner", "new pass")
        self.assertIn(str(self.store_id), self.service.get_managed_stores())

    def test_add_new_owner_sad(self):
        self.assertFalse(self.service.add_new_store_owner("not new owner", self.store_id))
        self.test_add_new_owner_success()
        self.service.logout()
        self.service.login("owner", "pass")
        self.assertFalse(self.service.add_new_store_owner("new owner", self.store_id))

    def test_add_new_owner_bad(self):
        self.assertFalse(self.service.add_new_store_owner("not new owner", self.store_id+40))


if __name__ == '__main__':
    unittest.main()
