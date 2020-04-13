from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from spellchecker import SpellChecker




class StoresManagerInterface:
    def __init__(self, users_manager):
        self.stores_manager = StoresManager()
        self.spell_checker = SpellChecker()
        self.users_manager = users_manager

    def get_store(self, store_id: int) -> Store:
        try:
            return self.stores_manager.get_store(store_id)
        except ValueError as e:
            print(e.args)

    def search_product(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) \
            -> {Store: [Product]}:
        """

        Args:
            search_term:
            categories:
            key_words:

        Returns:

        """
        return self.stores_manager.search(self.spell_checker.correction(search_term),
                                          [self.spell_checker.correction(word) for word in categories],
                                          [self.spell_checker.correction(word) for word in key_words])

    def add_purchase_to_store(self, store_id: int, purchase: Purchase):
        self.stores_manager.add_purchase_to_store(store_id, purchase)

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> {Store: [Product]}:
        return self.stores_manager.search(search_term, categories, key_words)

    def add_product_to_store(self, store_id: int, user_name: str, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str]) -> bool:
        if store_id in self.users_manager.get_stores(user_name):
            return self.stores_manager.add_product_to_store(store_id, user_name, product_name, product_price,
                                                            product_categories, key_words)
        return False

    def appoint_manager_to_store(self, store_id, owner, to_appoint):
        if store_id in self.users_manager.get_stores(owner) and self.users_manager.check_if_registered(to_appoint):
            self.stores_manager.appoint_manager_to_store(store_id, owner, to_appoint)

    def appoint_owner_to_store(self, store_id, owner, to_appoint):
        if store_id in self.users_manager.get_stores(owner) and self.users_manager.check_if_registered(to_appoint):
            self.stores_manager.appoint_owner_to_store(store_id, owner, to_appoint)

    def add_permission_to_manager_in_store(self, store_id, owner, manager, permission: str):
        if store_id in self.users_manager.get_stores(owner) and store_id in self.users_manager.get_stores(manager):
            self.stores_manager.add_permission_to_manager_in_store(store_id, owner, manager, permission)

    def remove_permission_from_manager_in_store(self, store_id, owner, manager, permission: str):
        if store_id in self.users_manager.get_stores(owner) and store_id in self.users_manager.get_stores(manager):
            self.stores_manager.remove_permission_from_manager_in_store(store_id, owner, manager, permission)

    def open_store(self, owner: str, store_name):
        if self.users_manager.check_if_registered(owner):
            store_id = self.stores_manager.open_store(owner, store_name)
            self.users_manager.add_store(owner, store_id)

    def buy(self, cart):
        self.stores_manager.buy(cart)
