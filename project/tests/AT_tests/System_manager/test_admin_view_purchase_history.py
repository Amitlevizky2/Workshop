import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class admin_view_purchase_history(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.register("admin", "1234")
        self.service.login("admin", "1234")
        self.service.logout()

    def test_admin_view_happy(self):
        self.service.register("user", "pass")
        if self.service.login("user", "pass"):
            res = self.service.searchProduct("Banana")
            first_store_id = list(res)[0]
            self.service.add_product(first_store_id, res.get(first_store_id)[0], 2)
            self.service.buy()
            result = self.service.get_purchase_history()
            self.service.logout()
            self.service.login("admin", "1234")
            history = self.service.view_store_history(self.store_id)
            self.assertIn( "Banana", result[0].products.keys())
            self.assertIsNotNone(history)
            self.assertIn("Banana", history[0].products.keys())

    def test_admin_view_sad(self):
        res = self.service.searchProduct("Apple")
        first_store_id = list(res)[0]
        self.service.add_product(first_store_id, res.get(first_store_id)[0], 2)
        self.service.buy()
        result = self.service.get_purchase_history()
        self.service.logout()
        self.service.login("admin", "1234")
        self.assertNotIn("apple", result[0].products.keys())

    def test_admin_view_bad(self):
        history = None
        self.service.logout()
        if self.service.admin:
            history = self.service.view_store_history(self.store_id)
        self.assertIsNone(history)


if __name__ == '__main__':
    unittest.main()
