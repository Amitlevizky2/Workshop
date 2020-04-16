import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP



class View_store_Products(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)

    def test_view_products_happy(self):
        res = self.service.searchProduct(("Apple", 20, "Food", "Fruits", 10))

    def test_view_products_sad(self):
        self.assertin(self.product2, self.store1.inventory)

    def test_view_products_bad(self):
        self.assertin(None, self.store1.inventory)


if __name__ == '__main__':
    unittest.main()
