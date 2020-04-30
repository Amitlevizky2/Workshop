
import unittest

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP
import jsonpickle



class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.register("username", "password")
        self.service.login("username", "password")
        res = self.service.searchProduct("Banana")
        res_dec = jsonpickle.decode(res)
        # product = res_dec
        self.first_store_id = list(res_dec)[0]
        encoded_product = jsonpickle.encode(res_dec.get(self.first_store_id)[0])
        self.service.add_product(self.first_store_id, encoded_product, 2)
        self.service.buy()
        self.result1 = jsonpickle.decode(self.service.get_purchase_history())
    def test_browse_happy(self):








if __name__ == '__main__':
    unittest.main()
