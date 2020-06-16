from unittest import TestCase

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Inventory import Inventory
import unittest


if __name__ == '__main__':
    unittest.main()


class TestInventory(TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.products["orange"] = Product("orange", 2, "food", None, 6)
        self.inv.products["Banana"] = Product("Banana", 2, "food", None, 2)
        self.inv.products["Tako"] = Product("Tako", 2, "food", None, 2)
        self.inv.products["Bamba"] = Product("Bamba", 2, "food", None, 2)
        self.inv.products["Potato"] = Product("Potato", 2, "food", None, 2)
        self.products_list = ["orange", "Banana", "Tako", "Bamba", "Potato"]

    def test_add_product(self):
        apple = Product("apple", 1, "food", None, 2)
        self.inv.add_product(apple.name, Product("apple", 1, "food", None, 2))
        inv_apple = self.inv.products.get(apple.name)
        self.assertTrue(apple == inv_apple)

    def test_buy_product(self):
        self.assertFalse(self.inv.buy_product("not real product", 1000))
        self.assertTrue(self.inv.buy_product("orange", 5))
        self.assertFalse(self.inv.buy_product("orange", 2))

    def test_get_products(self):
        for product in self.products_list:
            self.assertIn(product, self.inv.get_products())
        self.assertEqual(len(self.inv.get_products()), 5)

    def test_remove_product(self):
        self.assertIn("orange", self.inv.products.keys())
        self.inv.remove_product("orange")
        self.assertNotIn("orange", self.inv.products.keys())
