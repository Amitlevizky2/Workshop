import os
import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP
from datetime import datetime
import jsonpickle
import jsons
from project.data_access_layer import Base, meta, engine

class purchase_products_by_discount_types(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        res = self.service.searchProduct("Banana")
        res_dec = jsons.loads(res)
        # product = res_dec
        self.first_store_id = res_dec['avishop']["store_id"]
        self.service.add_product(self.first_store_id, "Banana", 2)
        self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)
        self.result0,self.result1 = self.service.get_purchase_history()
        self.happy = False
        self.sad = False
    @classmethod
    def tearDownClass(cls):
        os.remove("C:\\Users\\Owner\\Desktop\\Sadna_project\\Workshop\\daldal.db")




    def test_buy_by_type_purchase_happy(self):
        dis1 = self.service.add_discount_to_product(self.first_store_id,"avi","2018-11-12", "2021-11-12", 30,["Banana"])
        self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)
        result0, result2 = self.service.get_purchase_history()

        self.assertNotEqual(self.result1[0].products["Banana"]["original_price"], result2[0].products["Banana"]["price_after_disc"])
        self.happy = True
    def test_buy_by_type_purchase_sad(self):

        dis = self.service.add_discount_to_product(self.first_store_id, "Banana", "avi","2018-11-12",
                                                   "2021-11-12", 0)
        self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)
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
