import unittest
import mock
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager


class test_StoresManager(unittest.TestCase):
    def setUp(self) -> None:
        self.store_manager = StoresManager()
        self.idx = 0
        self.products = [
            ("t-shirt", 20, ["cloth"], ["green"], 7),
            ("apple", 1, ["food", "green"], ["vegetable"], 10),
            ("orange", 1, ["food", "orange"], ["fruits"], 10),
            ("iphone", 5000, ["electronics", "bag and expensive phone "], ["fruits"], 10)
        ]

    def test_update_product(self):
        with mock.patch('project.domain_layer.stores_managment.Store'):
            pass

    def test_search(self):
        assert False

    def test_get_store(self):
        assert False

    def test_add_product_to_store(self):
        # check when store does not exit
        self.assertFalse(self.store_manager.add_product_to_store(-1, "moshe", "p", 1, "s", "e", 10))

        # add some products
        for product in self.products:
            self.test_open_store()
            self.assertTrue(
                self.store_manager.add_product_to_store(self.idx - 1, "moshe" + str(self.idx - 1), *product))
            # check if added successfully
            self.assertIn(product[0], self.store_manager.get_store(self.idx - 1).inventory.products.keys())

        # check add product without permission
        product = self.products[0]
        self.assertFalse(
            self.store_manager.add_product_to_store(self.idx - 1, "not moshe" + str(self.idx - 1), *product))

    def test_appoint_manager_to_store(self):
        assert False

    def test_appoint_owner_to_store(self):
        assert False

    def test_add_permission_to_manager_in_store(self):
        assert False

    def test_remove_permission_from_manager_in_store(self):
        assert False

    def test_add_purchase_to_store(self):
        assert False

    def test_open_store(self):
        self.assertEqual(self.idx,
                         self.store_manager.open_store("moshe" + str(self.idx), "moshe's store" + str(self.idx)))

        self.assertIn(self.idx, self.store_manager.stores.keys())
        self.idx += 1

    def test_buy(self):
        assert False

    def test_get_sales_history(self):
        assert False


if __name__ == '__main__':
    unittest.main()
