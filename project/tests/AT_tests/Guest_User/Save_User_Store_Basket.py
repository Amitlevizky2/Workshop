import unittest

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP

class Save_basket_Store(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)


    def test_save_basket_happy(self):
        res = self.service.searchProduct("Banana")
        first_store_id = list(res)[0]
        res1 = self.service.add_product(first_store_id,"banana",1)
        self.assertEqual(res1.products[0], "banana")


    def test_save_basket_sad(self):
        pass


if __name__ == '__main__':
    unittest.main()
