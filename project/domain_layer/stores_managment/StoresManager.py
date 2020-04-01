from project.domain_layer.stores_managment.Store import Store


class StoreManager:
    def __init__(self):
        self.stores = {}[int, Store]
        self.stores_idx = 0

    def search(self, product_name: str = "", category: list[str] = None, key_word: list[str] = None):
        product_to_store = []
        for store in self.stores.keys():
            product_to_store.append(
                (self.stores.get(store), self.stores.get(store).search_product(product_name, category, key_word)))
