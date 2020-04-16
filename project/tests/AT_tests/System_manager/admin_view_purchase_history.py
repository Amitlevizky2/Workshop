import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP

class admin_view_purchase_history(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.register("admin","admin")
        self.service.login("admin","admin")


    def test_admin_view_happy(self):
        self.service.register("user", "pass")
        if self.service.login("user", "pass"):
            res = self.service.searchProduct("Banana")
            first_store_id = list(res)[0]
            self.service.add_product(first_store_id, res.get(first_store_id), 2)
            self.service.buy()
            if self.service.admin:
                    result = self.service.get_purchase_history()
                    history = self.service.view_store_history(self.store_id)
                    self.assertEqual(result.products[0].name, "Banana")
                    self.assertIsNotNone(history)
                    self.assertEqual("Apple", history.products[0].product_name)

    def test_admin_view_sad(self):
        if self.service.admin:
            res = self.service.searchProduct("apple")
            first_store_id = list(res)[0]
            self.service.add_product(first_store_id, res.get(first_store_id), 2)
            self.service.buy()
            result = self.service.get_purchase_history()
            self.assertNotEqual(result.products[0].name, "apple")

    def test_admin_view_bad(self):
        history = None
        self.service.logout()
        if self.service.admin:
            history = self.service.view_store_history(self.store_id)
        self.assertIsNone(history)







if __name__ == '__main__':
    unittest.main()
