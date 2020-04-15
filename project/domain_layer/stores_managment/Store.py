from project.domain_layer.external_managment.Purchase import Purchase
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
        self.appointed_by = {}

    def appoint_owner(self, owner, to_appoint):
        """

        Args:
            owner:
            to_appoint:

        Returns:

        """
        if owner in self.store_owners and \
                to_appoint not in self.store_owners:
            return self.appoint_owner_helper(owner, to_appoint)
        else:
            return False

    def appoint_owner_helper(self, owner, to_appoint):
        self.store_owners.append(to_appoint)
        if to_appoint in self.store_managers:
            self.store_managers.pop(to_appoint)

        if owner in self.appointed_by.keys():
            self.appointed_by[owner].append(to_appoint)

        else:
            self.appointed_by[owner] = [to_appoint]

        return True

    def remove_owner(self, owner, to_remove):

        """

        Args:
            owner:
            to_remove:

        Returns:

        """
        if owner in self.store_owners:
            if to_remove in self.store_owners:

                if owner in self.appointed_by.keys() and to_remove in self.appointed_by.get(owner):
                    if to_remove in self.appointed_by.keys():
                        self.appointed_by[owner].remove(to_remove)
                        self.__remove_owner_all_appointed(to_remove)

                    return True
                else:
                    return False
            else:
                return False

        else:
            return False

    def remove_manager(self, owner, to_remove):

        """

        Args:
            owner:
            to_remove:

        Returns:

        """
        if owner in self.store_owners:
            if to_remove in self.store_managers.keys():

                if to_remove in self.appointed_by.get(owner):

                    self.appointed_by[owner].remove(to_remove)
                    self.store_managers.pop(to_remove)

                    return True
                else:
                    return False
            else:
                return False

        else:
            return False

    def __remove_owner_all_appointed(self, to_remove):

        if to_remove in self.store_owners:
            self.store_owners.remove(to_remove)
        if to_remove in self.store_managers.keys():
            self.store_managers.pop(to_remove)
        if to_remove in self.appointed_by.keys():
            for own_or_man in self.appointed_by[to_remove]:
                self.__remove_owner_all_appointed(own_or_man)
                self.appointed_by.pop(to_remove)

    def add_permission_to_manager(self, owner, manager, permission):
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

    def remove_permission_from_manager(self, owner, manager, permission):
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
                if permission_function in self.store_managers.get(manager):
                    self.store_managers[manager].remove(permission_function)
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
            if owner in self.appointed_by.keys():
                self.appointed_by[owner].append(to_appoint)
            else:
                self.appointed_by[owner] = [to_appoint]
            return True
        else:
            return False

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories,
                    key_words: [str], amount) -> bool:
        """

        Args:
            user_name:the user who wants to add product, should be a owner
                or a manager with permission
            product_name:product name
            product_price:product price
            product_categories:
            key_words:

        Returns:

        """
        if self.check_permission(user_name, self.add_product):
            self.inventory.add_product(product_name,
                                       Product(product_name, product_price, product_categories, key_words, amount))
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
                result.append(self.inventory.products.get(product_name))
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

    def buy_product(self, product_name, amount):
        self.inventory.buy_product(product_name, amount)

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        if self.check_permission(user, self.get_sales_history) or is_admin:
            return self.sales

    def update_product(self, user, product_name, attribute, updated):
        if self.check_permission(user, self.update_product):
            self.inventory.update_product(product_name, attribute, updated)
            return True
        return False
    def add_new_sale(self, purchase: Purchase) -> bool:
        """

         Args:

             purchase: Holds the store products bought by the user
         Returns:
                 True if @new_sale was added to @self.sales list, else false
         """
        if self.sales.append(purchase) is None:
            return True
        return False

    def check_permission(self, user, function):
        return user in self.store_owners or \
               (user in self.store_managers and function in self.store_managers.get(user))
