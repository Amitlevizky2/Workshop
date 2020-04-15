import unittest
from unittest import mock
from unittest.mock import patch
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager


class test_StoresManager(unittest.TestCase):

    def setUp(self) -> None:
        stores = [
            ("moshe", "test_store"),
            ("moshe", "test_store1"),
            ("levitsky", "loser's store")
        ]
        products_for_stores = [
            [
                ("apple", 1, ["food", "green"], ["vegetable"], 10),
                ("orange", 1, ["food", "orange"], ["fruits"], 10),
                ("iphone", 5000, ["electronics", "bag and expensive phone "], ["fruits"], 10)
            ],
            [
                ("t-shirt", 20, ["cloth"], ["green"], 7),
            ]
        ]
        self.stores_manager = StoresManager()
        for store in stores:
            self.stores_manager.open_store(*store)
        for index in range(len(stores)):
            for products in products_for_stores:
                for product in products:
                    self.stores_manager.add_product_to_store(index, stores[index][0], *product)

    def test_update_product(self):
        with patch.object(Store, 'update_product') as mock_store:
            mock_store.return_value = True
            self.assertTrue(self.stores_manager.update_product(0, "moshe", "apple", "price", 2))
            mock_store.return_value = False
            self.assertFalse(self.stores_manager.update_product(0, "s", "w", "price", 20))
            print("hi")

    def test_Buy(self):

        pass

if __name__ == '__main__':
    unittest.main()
