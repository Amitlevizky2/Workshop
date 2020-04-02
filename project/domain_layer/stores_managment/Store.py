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
        self.store_managers = {}  # {manager_name:functions}
        self.sales = []
        self.rate = 0

    def appoint_owner(self, owner, to_appoint):
        """

        Args:
            owner:
            to_appoint:

        Returns:

        """
        if owner in self.store_owners:
            self.store_owners.append(to_appoint)
            return True
        else:
            return False

    def add_permission_to_manager(self, owner, manager, permission: str):
        """

        Args:
            owner:
            manager:
            permission:

        Returns:

        """
        if owner in self.store_owners:
            if manager in self.store_managers.keys():
                permission_function = getattr(Store, permission)
                if permission_function not in self.store_managers.get(manager):
                    self.store_managers[manager].append(permission_function)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def appoint_manager(self, owner, to_appoint):
        """

        Args:
            owner: user that in the owners list
            to_appoint: user that should be appoint to manager

        Returns:

        """
        if owner in self.store_owners and to_appoint not in self.store_managers.keys():
            self.store_managers[to_appoint] = [self.get_sales_history]
            return True
        else:
            return False

    def add_product(self, user: User, product_name: str, product_price: int, product_categories,
                    key_words: [str]) -> bool:
        """

        Args:
            user:the user who wants to add product, should be a owner
                or a manager with permission
            product_name:product name
            product_price:product price
            product_categories:
            key_words:

        Returns:

        """
        if self.check_permission(user, self.add_product):
            self.inventory.add_product(product_name, Product(product_name, product_price, product_categories, key_words))
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

    def get_sales_history(self, user) -> [(str, Basket)]:
        if self.check_permission(user, self.get_sales_history):
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

    def check_permission(self, user, function):
        return user in self.store_owners or \
               (user in self.store_managers and function in self.store_managers.get(user))
