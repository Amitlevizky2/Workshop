from project.domain_layer.stores_managment.Product import Product
from .Inventory import Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()

    def tearDown(self) -> None:
        self.inv.products = {}

    def test_add_product(self):

        apple = Product("apple", 1, "food", None)
        self.inv.add_product(apple.name, Product("apple", 1, "food", None))
        inv_apple = self.inv.products.get(apple.name)[0]
        self.assertTrue(apple == inv_apple)

    if __name__ == '__main__':
        unittest.main()
