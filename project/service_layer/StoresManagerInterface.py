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
