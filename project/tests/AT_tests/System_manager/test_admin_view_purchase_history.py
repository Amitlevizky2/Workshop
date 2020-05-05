import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP
import jsonpickle

class admin_view_purchase_history(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.register("admin", "1234")
        self.service.login("admin", "1234")
        self.service.logout()

    def test_admin_view_happy(self):
        res = jsonpickle.decode(self.service.searchProduct("Banana"))
        first_store_id = list(res)[0]
        enc_res = jsonpickle.encode(res.get(first_store_id)[0])
        self.service.add_product(first_store_id, enc_res, 2)
        self.service.buy()
        result = jsonpickle.decode(self.service.get_purchase_history())
        self.service.logout()
        self.service.login("admin", "1234")
        history = jsonpickle.decode(self.service.view_store_history(self.store_id))
        self.assertIn("Banana", result[0].products.keys())
        self.assertIsNotNone(history)
        self.assertIn("Banana", history[0].products.keys())


    def test_admin_view_sad(self):
        res = jsonpickle.decode(self.service.searchProduct("Apple"))
        first_store_id = list(res)[0]
        self.service.add_product(first_store_id, jsonpickle.encode(res.get(first_store_id)[0]), 2)
        self.service.buy()
        result = jsonpickle.decode(self.service.get_purchase_history())
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
