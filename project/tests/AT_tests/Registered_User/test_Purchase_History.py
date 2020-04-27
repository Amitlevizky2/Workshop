import unittest

import jsonpickle

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class purchase_History(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        self.service.register("user", "pass")
        self.service.login("user", "pass")
        res = self.service.searchProduct("Banana")
        res_dec = jsonpickle.decode(res)
        # product = res_dec
        first_store_id = list(res_dec)[0]
        encoded_product = jsonpickle.encode(res_dec.get(first_store_id)[0])
        self.service.add_product(first_store_id, encoded_product, 2)#TODO
        self.service.buy()

    def test_purchase_happy(self):
        result = jsonpickle.decode(self.service.get_purchase_history())
        self.assertEqual(list(result[0].products)[0], "Banana")

    def test_purchase_bad(self):
        self.service.logout()
        result = jsonpickle.decode(self.service.get_purchase_history())
        self.assertTrue(len(result) == 0)

    def test_purchase_sad(self):
        res1 = jsonpickle.decode(self.service.get_purchase_history())
        self.assertNotEqual(list(res1[0].products)[0], "marshmelo")



if __name__ == '__main__':
    unittest.main()
