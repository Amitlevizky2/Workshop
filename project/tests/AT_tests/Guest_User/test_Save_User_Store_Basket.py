import unittest

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP
import jsonpickle

class Save_basket_Store(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)

        self.service.register("user", "pass")
        self.service.login("user", "pass")
        res = jsonpickle.decode(self.service.searchProduct("Banana"))
        first_store_id = list(res)[0]
        enc = jsonpickle.encode(res.get(first_store_id)[0])
        self.service.add_product(first_store_id, enc, 2)
        self.service.buy()
    def test_save_basket_happy(self):
        result = jsonpickle.decode(self.service.get_purchase_history())
        self.assertIn("Banana", result[0].products)
    def test_save_basket_sad(self):
        result = jsonpickle.decode(self.service.get_purchase_history())
        x = 5
        self.assertNotIn("banana", result[0].products)



if __name__ == '__main__':
    unittest.main()
