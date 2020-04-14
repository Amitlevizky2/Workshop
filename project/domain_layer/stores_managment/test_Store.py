import unittest

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store(0, "test store", "test owner")
        self.store.store_managers = {"Moshe": [],
                                     "Amit": [Store.add_product],
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

    def test_add_permission_to_manager_one(self):
        # Sebastian is not in store managers dictionary
        self.assertFalse(self.store.remove_manager("test store", "Sebastian"))

        self.appoint_users_to_managers()
        # Check that 3 managers was added to managers dictionary
        for i in range(0, len(self.standard_users)):
            self.assertIn(self.standard_users[i], self.store.store_managers)

        # Amit is not owner
        self.assertFalse(self.store.add_permission_to_manager("Amit", "Lielle", "add_product"))

        # add_product is already in Amit permissions
        self.assertFalse(self.store.add_permission_to_manager("test owner", "Amit", "add_product"))

    def test_add_permission_to_manager_two(self):
        self.appoint_users_to_managers()
        # Check that 3 managers was added to managers dictionary
        for i in range(0, len(self.standard_users)):
            self.assertIn(self.standard_users[i], self.store.store_managers)

        # Valid parameters to the add permission method, Alex will get the add product permission
        self.assertTrue(self.store.add_permission_to_manager("test owner", "Alex", "add_product"))

        # Add product permission should now be in Alex's permissions
        self.assertIn(Store.add_product, self.store.store_managers["Alex"])

        # TODO: Only owner that appointed the manager can give him permissions

    def test_remove_permission_from_manager_one(self):
        # Amit is not an owner
        self.assertFalse(self.store.remove_permission_from_manager("Amit", "Evgeny", "add_product"))

        # Ron is not a manager, mannnn, that's a bummer
        self.assertFalse(self.store.remove_permission_from_manager("test owner", "Ron", "add_product"))

        self.appoint_users_to_managers()
        # You know that Ron does not have that permission, don't you?!
        self.assertFalse(self.store.remove_permission_from_manager("test owner", "Ron", "add_product"))

    def test_remove_permission_from_manager_two(self):
        self.appoint_users_to_managers()
        self.store.appoint_owner("test owner", "Moshe")
        self.store.add_permission_to_manager("test owner", "Avishay", "add_product")

        # Don't be blind dude, I just added Avishay's permissions the add product permission
        self.assertIn(Store.add_product, self.store.store_managers["Avishay"])

        #TODO: Only owner that appointed the manager can remove his permissions

        # Moshe, it is really not your business what permissions Avishay have, Let it go.
        # self.assertFalse(self.store.remove_permission_from_manager("Moshe", "Avishay", "add_product"))

        # Look Avishay, it's is not you, its me, I'm taking this permission from you, I'm sorry
        self.assertTrue(self.store.remove_permission_from_manager("test owner", "Avishay", "add_product"))

        # Just wanna make sure you don't hide from this permission again man
        self.assertNotIn(Store.add_product, self.store.store_managers["Avishay"])

        # Ok, last time I swear
        self.assertFalse(self.store.remove_permission_from_manager("test owner", "Avishay", "add_product"))

    def test_appoint_manager_one(self):
        # Well, Moshe  you are not an owner yet, so...
        self.assertFalse(self.store.appoint_manager("Moshe", "Alex"))

        # Evgeny, you need to come back to earth and now!, you are already a manager man
        self.assertFalse(self.store.appoint_manager("test owner", "Evgeny"))

    def test_appoint_manager_two(self):
        # Welcome Ron, a whole new world is waiting for
        self.assertTrue(self.store.appoint_manager("test owner", "Ron"))

        # Yeah well i"ll check for you if you were added to the managers list, chill out man
        self.assertIn("Ron", self.store.store_managers.keys())

        # Ok, test owner is so annoying! he makes me check that its recorded that you were appointed by him
        self.assertIn("Ron", self.store.appointed_by["test owner"])

        # Now that you become a manager, let see if you can see the store sales history
        self.assertIn(Store.get_sales_history, self.store.store_managers["Ron"])

    def appoint_managers_to_owners(self, users):
        for i in range(0, len(users) - 1):
            self.store.appoint_owner(users[i], users[i + 1])

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


if __name__ == '__main__':
    unittest.main()
