from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Inventory import Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.products = {"orange": Product("orange", 2, "food", None, 2)}

    def test_add_product(self):
        apple = Product("apple", 1, "food", None, 2)
        self.inv.add_product(apple.name, Product("apple", 1, "food", None, 2))
        inv_apple = self.inv.products.get(apple.name)
        self.assertTrue(apple == inv_apple)

    def test_update_product(self):
        self.inv.update_product("orange", "price", 5)
        self.assertEqual(5, self.inv.products.get("orange").price)

    def test_remove_product(self):
        self.assertIn("orange", self.inv.products.keys())
        self.inv.remove_product("orange")
        self.assertNotIn("orange", self.inv.products.keys())

    def test_buy_product(self):
        self.assertFalse(self.inv.buy_product("not real product", 1000))
        self.assertFalse(self.inv.buy_product("orange", 5))
        self.assertTrue(self.inv.buy_product("orange", 2))


if __name__ == '__main__':
    unittest.main()
