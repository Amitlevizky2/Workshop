import unittest

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store(0, "test store", "test owner")

    def test_add_product(self):
        self.store.add_product("test owner", "apple", 1, ["food", "fruit"], ["green"])
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"])==self.store.inventory.products.get("apple")[0])

    def test_search(self):
        self.test_add_product()
        ap = self.store.search("apple")
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"]) == ap[0])
        ap = self.store.search(categories=["food"])
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"]) == ap[0])
        ap = self.store.search(key_words=["green"])
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"]) == ap[0])