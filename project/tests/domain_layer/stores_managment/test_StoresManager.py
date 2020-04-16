import unittest

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.NullStore import NullStore
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager


class StubStore(Store):

    def appoint_owner(self, owner, to_appoint):
        return super().appoint_owner(owner, to_appoint)

    def appoint_owner_helper(self, owner, to_appoint):
        return super().appoint_owner_helper(owner, to_appoint)

    def remove_owner(self, owner, to_remove):
        return super().remove_owner(owner, to_remove)

    def remove_manager(self, owner, to_remove):
        return super().remove_manager(owner, to_remove)

    def add_permission_to_manager(self, owner, manager, permission):
        return super().add_permission_to_manager(owner, manager, permission)

    def remove_permission_from_manager(self, owner, manager, permission):
        return super().remove_permission_from_manager(owner, manager, permission)

    def appoint_manager(self, owner, to_appoint):
        return super().appoint_manager(owner, to_appoint)

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories, key_words: [str],
                    amount) -> bool:
        if user_name != "test_owner" + str(self.store_id):
            return False
        return True

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
        if self.store_id == 4 and search_term == "":
            return []
        return [Product("Banana", 2, ["fruit"], ["fruits"], 2)]

    def buy_product(self, product_name, amount):
        super().buy_product(product_name, amount)

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        return super().get_sales_history(user, is_admin)

    def update_product(self, user, product_name, attribute, updated):
        return product_name != "not real product"

    def add_new_sale(self, purchase: Purchase) -> bool:
        return super().add_new_sale(purchase)

    def check_permission(self, user, function):
        return super().check_permission(user, function)

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

    
    def test_appoint_manager_to_store(self):
        pass

    def test_appoint_owner_to_store(self):
        pass

    def test_add_permission_to_manager_in_store(self):
        pass

    def test_remove_permission_from_manager_in_store(self):
        pass

    def test_add_purchase_to_store(self):
        pass

    def test_open_store(self):
        pass

    def test_buy(self):
        pass

    def test_get_sales_history(self):
        pass


if __name__ == '__main__':
    unittest.main()
