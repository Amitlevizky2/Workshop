from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class StoreManager:
    def __init__(self):
        self.stores = {int: Store}
        self.stores_idx = 0

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> {int: [Product]}:
        search_result = {}
        for store_id in self.stores.keys():
            search_in_store = self.stores.get(store_id).search(search_term, categories, key_words)
            if search_in_store is not None:
                search_result[store_id] = search_in_store
        return search_result
