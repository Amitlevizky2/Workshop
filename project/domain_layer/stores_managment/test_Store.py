import unittest

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store(0, "test store", "test owner")
        self.store.store_managers["Moshe"] = []

    def test_appoint_owner_one(self):
        # There is no such owner
        self.assertFalse(self.store.appoint_owner("not test owner", "Moshe"))
        # Valid appointment
        self.assertTrue(self.store.appoint_owner("test owner", "Moshe"))
        # Moshe is already a store owner, should not e appointed again
        self.assertFalse(self.store.appoint_owner("test owner", "Moshe"))

    def test_appoint_owner_two(self):
        self.store.appoint_owner("test owner", "Moshe")
        # to_appoint is already owner of the store
        self.assertFalse(self.store.appoint_owner("test owner", "test owner"))
        # If Moshe was a manager, pull him out from that list
        self.assertNotIn("Moshe", self.store.store_managers)
        # Moshe become part of the owners list
        self.assertIn("Moshe", self.store.store_owners)
        # Validate that Moshe was appointed by test owner and now become his appointee
        self.assertIn("Moshe", self.store.appointed_by["test owner"])

    def test_add_product(self):
        self.store.add_product("test owner", "apple", 1, ["food", "fruit"], ["green"], 2)
        self.assertTrue(
            Product("apple", 1, ["food", "fruit"], ["green"], 2) == self.store.inventory.products.get("apple"))
        pass

    def test_search(self):
        self.test_add_product()
        ap = self.store.search("apple")
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"], 2) == ap[0])
        ap = self.store.search(categories=["food"])
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"], 2) == ap[0])
        ap = self.store.search(key_words=["green"])
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"], 2) == ap[0])



    def test_add_permission_to_manager(self):
        self.store.appoint_manager("test owner", "michael")
        self.assertFalse(self.store.check_permission("michael", Store.add_product))
        self.store.add_permission_to_manager("test owner", "michael", "add_product")
        ans = self.store.check_permission("michael", Store.add_product)
        self.assertTrue(ans)

    def test_appoint_manager(self):
        self.assertFalse(self.store.appoint_owner("not test owner", "michael"))
        self.assertTrue(self.store.appoint_owner("test owner", "michael"))

    def test_get_sales_history(self):
        pass

    def test_add_new_sale(self):
        pass

    def test_check_permission(self):
        pass

    def test_remove_owner(self):
        self.store.appoint_owner("test owner", "moshe")
        self.assertFalse(self.store.remove_owner("moshe", "test owner"))
        self.assertTrue(self.store.remove_owner("test owner", "moshe"))

    def test_remove_manager(self):
        self.store.appoint_manager("test owner", "moshe")
        self.assertFalse(self.store.remove_manager("moshe", "test owner"))
        self.assertTrue(self.store.remove_manager("test owner", "moshe"))

    def test_remove_permission_from_manager(self):
        self.store.appoint_manager("test owner", "moshe")
        self.assertFalse(self.store.check_permission("moshe", Store.add_product))
        self.store.add_permission_to_manager("test owner", "moshe", "add_product")
        ans = self.store.check_permission("moshe", Store.add_product)
        self.assertTrue(ans)
        self.store.remove_permission_from_manager("test owner", "moshe", "add_product")
        ans = self.store.check_permission("moshe", Store.add_product)
        self.assertFalse(ans)


if __name__ == '__main__':
    unittest.main()
