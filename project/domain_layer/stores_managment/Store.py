from project.domain_layer.stores_managment.Inventory import Inventory
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.users_managment import User, Basket


class Store:
    def __init__(self, store_id, name, store_owner):
        self.id = store_id
        self.name = name
        self.inventory = Inventory()
        self.sale_policy = None
        self.discount_policy = None
        self.store_owners = [store_owner]
        self.sales = []
        self.rate = 0

    def add_product(self, user: User, product_name: str, product_price: int, product_category,
                    key_words: [str]) -> bool:
        """

        Args:
            user:
            product_name:
            product_price:
            product_category:
            key_words:

        Returns:

        """
        if user in self.store_owners:
            self.inventory.add_product(product_name, Product(product_name, product_price, product_category, key_words))
            return True
        else:
            return False

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
        """

        Args:
            search_term: part of the wanted product name
            categories: categories to search in
            key_words:
        Returns:
                list of products
        """
        result = []
        for product_name in self.inventory.products.keys():
            if search_term in product_name:
                result.append(self.inventory.products.get(product_name)[0])
        if categories is not None:
            for product in result:
                for category in categories:
                    if category not in product.categories:
                        result.remove(product)

        if key_words is not None:
            for product in result:
                for word in key_words:
                    if word not in product.key_words:
                        result.remove(product)
        return result

    def get_sales_history(self) -> [(str, Basket)]:
        return self.sales

    def add_new_sale(self, user_id, basket) -> bool:
        """

         Args:
             user_id: The user who made the purchase
             basket: Holds the store products bought by the user
         Returns:
                 True if @new_sale was added to @self.sales list, else false
         """
        if self.sales.append((user_id, basket)) is None:
            return True
        return False
