import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP
import jsonpickle


class View_store_Products(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        self.service.register("user", "pass")
        self.service.login("user","pass")
        self.store_Id = self.service.Open_store("store")
        self.service.add_product_to_Store(self.store_Id,"grape",50,"fruits","little",50)
    def test_view_products_happy(self):
        res = jsonpickle.decode(self.service.searchProduct("grape"))
        x=5
        self.assertIn("grape", res['1'][0].name)

    def test_view_products_sad(self):
        res = jsonpickle.decode(self.service.searchProduct("Grape"))
        x=5
        self.assertNotEqual(res,"greape")



if __name__ == '__main__':
    unittest.main()
