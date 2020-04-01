from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class StoresManagerInterface:
    def __init__(self):
        self.stores_manager = StoresManager()

    def search_product(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) \
            -> {Store: [Product]}:
        """

        Args:
            search_term:
            categories:
            key_words:

        Returns:

        """
        return self.stores_manager.search(search_term, categories, key_words)
