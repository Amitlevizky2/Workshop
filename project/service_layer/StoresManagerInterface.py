from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from spellchecker import SpellChecker


class StoresManagerInterface:
    def __init__(self):
        self.stores_manager = StoresManager()
        self.spell_checker = SpellChecker()

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
