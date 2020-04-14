import unittest

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store(0, "test store", "test owner")
        self.store.store_managers = {"Moshe": [],
                                     "Amit": [],
                                     "Hadar": [],
                                     "Lielle": [],
                                     "Noa": [],
                                     "Evgeny": []}
        self.standard_users = ["Avishay",
                               "Alex",
                               "Ron"]

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

    def test_remove_owner_one(self):
        users = [*self.store.store_managers]
        self.store.appoint_owner("test owner", "Moshe")
        self.appoint_managers_to_owners(users)

        #owner is not really a store owner
        self.assertFalse(self.store.remove_owner("Sebastian", "Amit"))
        #to_remove is not a store owner
        self.assertFalse(self.store.remove_owner("Amit", "Sebastian"))
        #to_remove was not appointed by owner
        self.assertFalse(self.store.remove_owner("Amit", "Lielle"))

    def test_remove_owner_two(self):
        users = [*self.store.store_managers]
        self.store.appoint_owner("test owner", "Moshe")
        self.appoint_managers_to_owners(users)

        # Check that all of the owner that was appoint by Moshe will are in the owners list
        for i in range(0, len(users)):
            self.assertIn(users[i], self.store.store_owners)

        # Check that every appointed owner is in the appointed by list of his appointee
        for i in range(0, len(users) - 1):
            self.assertIn(users[i + 1], self.store.appointed_by[users[i]])

        self.store.remove_owner("test owner", "Moshe")
        # Check that all of the owner that was appoint by Moshe will be deleted
        for i in range(0, len(users)):
            self.assertNotIn(users[i], self.store.store_owners)

        # Check that every appointed owner is not in the appointed by list of his appointee
        for i in range(0, len(users)):
            self.assertNotIn(users[i], self.store.appointed_by)

    def appoint_managers_to_owners(self, users):
        for i in range(0, len(users) - 1):
            self.store.appoint_owner(users[i], users[i+1])

    def test_remove_manager_one(self):
        self.store.appoint_owner("test owner", "Moshe")
        self.store.appoint_manager("Moshe", "Hadar")

        # Amit is not owner
        self.assertFalse(self.store.remove_manager("Amit", "Lielle"))
        # Sebastian is not in store managers dictionary
        self.assertFalse(self.store.remove_manager("test store", "Sebastian"))
        # Hadar was not appointed by test owner
        self.assertFalse(self.store.remove_manager("test store", "Hadar"))

    def test_remove_manager_two(self):
        self.appoint_users_to_managers()
        # Check that 3 managers was added to managers dictionary
        for i in range(0, len(self.standard_users)):
            self.assertIn(self.standard_users[i], self.store.store_managers)

        # Avishay should be in the appointed by test owner list
        self.assertIn("Avishay", self.store.appointed_by["test owner"])
        # test owner and Avishay are valid parameters to the method
        self.assertTrue(self.store.remove_manager("test owner", "Avishay"))
        # Avishay should not be in store's mangers list.
        self.assertNotIn("Avishay", self.store.store_managers)
        # Avishay should not be in the appointed by test owner list
        self.assertNotIn("Avishay", self.store.appointed_by["test owner"])

    def appoint_users_to_managers(self):
        for i in range(0, len(self.standard_users)):
            self.store.appoint_manager("test owner", self.standard_users[i])

    def test_add_product(self):
        self.store.add_product("test owner", "apple", 1, ["food", "fruit"], ["green"], 2)
        self.assertTrue(
            Product("apple", 1, ["food", "fruit"], ["green"], 2) == self.store.inventory.products.get("apple"))
        pass

    def test_search(self):
        self.test_add_product()
        ap = self.store.search("apple")
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"],2) == ap[0])
        ap = self.store.search(categories=["food"])
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"],2) == ap[0])
        ap = self.store.search(key_words=["green"])
        self.assertTrue(Product("apple", 1, ["food", "fruit"], ["green"],2) == ap[0])

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
