import unittest

import jsonpickle

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.NullStore import NullStore
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager


class StubStore(Store):

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories, key_words: [str],
                    amount) -> bool:
        if user_name != "test_owner" + str(self.store_id):
            return False
        return True

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
        if self.store_id == 4 and search_term == "":
            return []
        return [Product("Banana", 2, ["fruit"], ["fruits"], 2)]

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        return ["hi,i'm a admin view purchase"] if is_admin else ["i'm no admin"]

    def update_product(self, user, product_name, attribute, updated):
        return product_name != "not real product"

    def __init__(self, idx, name, owner):
        Store.__init__(self, idx, name, owner)


class test_StoresManager(unittest.TestCase):
    def setUp(self) -> None:
        self.store_manager = StoresManager()
        for i in range(5):
            self.store_manager.stores[i] = StubStore(i, "test_store" + str(i), "test_owner" + str(i))
        self.store_manager.stores_idx = i

    def test_update_product(self):
        for store_id in self.store_manager.stores.keys():
            self.assertFalse(
                self.store_manager.update_product(store_id, "test_owner" + str(store_id), "not real product", "price",
                                                  20))
            self.assertTrue(
                self.store_manager.update_product(store_id, "test_owner" + str(store_id), "real product", "price",
                                                  20))

    def test_search(self):
        banana_search = jsonpickle.decode(self.store_manager.search("Banana"))
        self.assertEqual(len(banana_search), 5)
        fruit_search = jsonpickle.decode(self.store_manager.search(categories=["fruit"]))
        self.assertEqual(len(fruit_search), 4)

    def test_get_store(self):
        self.assertTrue(isinstance(self.store_manager.get_store(7), NullStore))
        self.test_open_store()
        self.assertTrue(2 == self.store_manager.get_store(2).store_id)

    def test_add_product_to_store(self):
        self.assertFalse(
            self.store_manager.add_product_to_store(7, "not real store", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20))
        self.assertFalse(
            self.store_manager.add_product_to_store(2, "test_owner", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20))
        self.assertTrue(
            self.store_manager.add_product_to_store(2, "test_owner2", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20))

    def test_open_store(self):
        index = self.store_manager.stores_idx
        self.store_manager.open_store("t_ownet", "test")
        self.assertEqual(index + 1, self.store_manager.stores_idx)

    def test_get_sales_history(self):
        self.assertListEqual(jsonpickle.decode(self.store_manager.get_sales_history(78, "the king", True)), [])
        self.assertEqual(jsonpickle.decode(self.store_manager.get_sales_history(0, "some owner", False))[0],
                         "i'm no admin")
        self.assertEqual(jsonpickle.decode(self.store_manager.get_sales_history(0, "some owner", True))[0],
                         "hi,i'm a admin view purchase")


if __name__ == '__main__':
    unittest.main()
