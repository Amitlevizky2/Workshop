import unittest
from unittest import mock
from unittest.mock import patch

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager


class test_StoresManager(unittest.TestCase):

    def setUp(self) -> None:
        self.stores_manager = StoresManager()

        self.stores_manager.open_store("s", "store")
        self.stores_manager.add_product_to_store(0, "s", "t", 2, None, None, 2)

    def test_update_product(self):
        with patch.object(Store, 'update_product') as mock_store:
            mock_store.return_value = True
            self.assertTrue(self.stores_manager.update_product(0, "s", "t", "price", 2))
            mock_store.return_value = False
            self.assertFalse(self.stores_manager.update_product(0, "s", "w", "price", 20))
            print("hi")


if __name__ == '__main__':
    unittest.main()



