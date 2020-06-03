import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP
import datetime
import jsonpickle


class purchase_products_by_discount_types(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        res = self.service.searchProduct("Banana")
        res_dec = jsonpickle.decode(res)
        # product = res_dec
        self.first_store_id = list(res_dec)[0]
        encoded_product = jsonpickle.encode(res_dec.get(self.first_store_id)[0])
        self.service.add_product(self.first_store_id, encoded_product, 2)
        self.service.buy()
        self.result1 = jsonpickle.decode(self.service.get_purchase_history())

    def test_buy_by_type_purchase_happy(self):
        dis1 = self.service.add_discount_to_product(self.first_store_id,"Banana","avi",datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 30)
        dis2 = self.service.add_discount_to_product(self.first_store_id, "Banana", "avi", datetime.datetime(2018, 6, 1),
                                                    datetime.datetime(2020, 5, 17), 30)
        dis3 = self.service.add_discount_to_product(self.first_store_id, "Banana", "avi", datetime.datetime(2018, 6, 1),
                                                    datetime.datetime(2020, 5, 17), 30)

        self.service.buy()
        result2 = jsonpickle.decode(self.service.get_purchase_history())
        self.assertNotEqual(self.result1[0].products["Banana"][0].get_price(), result2[0].products["Banana"][0].get_price())

    def test_buy_by_type_purchase_sad(self):

        dis = self.service.add_discount_to_product(self.first_store_id, "Banana", "avi", datetime.datetime(2018, 6, 1),
                                                   datetime.datetime(2020, 5, 17), 0)
        self.service.buy()
        result2 = self.service.get_purchase_history()
        self.assertEqual(self.result1[0].products["Banana"][0].get_price(), result2[0].products["Banana"][0].get_price())

    def test_buy_by_type_purchase_bad(self):
        res = self.service.searchProduct("Banana")
        first_store_id = list(res)[0]
        self.service.add_product(first_store_id, res.get(first_store_id)[0], 2)
        self.service.buy()
        result = self.service.get_purchase_history()
        self.service.logout()
        self.assertIn("Banana", result[0].products.keys())



if __name__ == '__main__':
    unittest.main()
