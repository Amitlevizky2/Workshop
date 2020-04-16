from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Inventory import Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.products = {"orange": Product("orange", 2, "food", None, 2)}

    def tearDown(self) -> None:
        self.inv.products = {}

    def test_add_product(self):
        apple = Product("apple", 1, "food", None,2)
        self.inv.add_product(apple.name, Product("apple", 1, "food", None, 2))
        inv_apple = self.inv.products.get(apple.name)
        self.assertTrue(apple == inv_apple)

    def test_update_product(self):
        self.inv.update_product("orange", "price", 5)
        self.assertEqual(5, self.inv.products.get("orange").price)


if __name__ == '__main__':
    unittest.main()
