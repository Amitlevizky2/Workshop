import unittest

import jsons

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP



class View_store_Products(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        self.service.register("user", "pass")
        self.service.login("user","pass")
        self.store_Id = self.service.Open_store("store")
        self.service.add_product_to_Store(self.store_Id,"grape",50,"fruits","little",50)
    def test_view_products_happy(self):
        res = self.service.searchProduct("grape")
        res=jsons.loads(res)
        self.assertEqual(res['store']['search_res'][0]['name'], "grape")



if __name__ == '__main__':
    unittest.main()
