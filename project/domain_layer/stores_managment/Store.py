from project.domain_layer.communication_managment.Publisher import Publisher
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies import ConditionalStoreDiscount, DiscountPolicy
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.Inventory import Inventory
from project.domain_layer.stores_managment.Product import Product
from project import logger
from project.domain_layer.stores_managment.PurchasesPolicies.PurchaseCompositePolicy import PurchaseCompositePolicy
from project.domain_layer.stores_managment.PurchasesPolicies.PurchaseProductPolicy import PurchaseProductPolicy
from project.domain_layer.stores_managment.PurchasesPolicies.PurchaseStorePolicy import PurchaseStorePolicy
from project.domain_layer.users_managment import Basket


class Store:
    def __init__(self, store_id, name, store_owner):
        self.store_id = store_id
        self.name = name
        self.inventory = Inventory()
        self.discounts = {}  # {discount_id: Discount}
        self.discount_idx = 0
        self.purchase_policies = {}  # {purchase_policy_id: PurchasePolicy}
        self.purchases_idx = 0
        self.store_owners = [store_owner]
        self.store_managers = {}  # {manager_name:functions}
        self.sales = []
        self.rate = 0
        self.appointed_by = {store_owner: []}

    def appoint_owner(self, owner, to_appoint):
        """

        Args:
            owner:
            to_appoint:

        Returns:

        """
        if owner in self.store_owners and \
                to_appoint not in self.store_owners:
            return {'ans': True,
                    'desc': self.appoint_owner_helper(owner, to_appoint)}
        else:
            logger.error("%s is not a store owner or %s is already owner", owner, to_appoint)
            return {'ans': False,
                    'desc': owner + "is not a store owner or " + to_appoint + " is already owner"}

    def appoint_owner_helper(self, owner, to_appoint):
        self.store_owners.append(to_appoint)
        self.appointed_by[to_appoint] = []
        if to_appoint in self.store_managers:
            self.store_managers.pop(to_appoint)
        self.appointed_by[owner].append(to_appoint)
        return True

    def remove_owner(self, owner, to_remove, publisher: Publisher):

        """

        Args:
            owner:
            to_remove:
            :param owner:
            :param to_remove:
            :param publisher:

        Returns:


        """
        if owner in self.store_owners:
            if to_remove in self.store_owners:
                if owner in self.appointed_by.keys() and to_remove in self.appointed_by.get(owner):
                    if to_remove in self.appointed_by.keys():
                        self.appointed_by[owner].remove(to_remove)
                        self.__remove_owner_all_appointed(to_remove, publisher)
                    return {'ans': True,
                            'desc': 'product has been removed'}
                else:
                    logger.error("%s is not a store owner", owner)
                    return {'ans': False,
                            'desc': to_remove + ' is not a appointed by ' + owner}
            else:
                return {'ans': False,
                        'desc': to_remove + ' is not owner of this store'}
        else:
            return {'ans': False,
                    'desc': to_remove + ' is not owner of this store'}

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

                    return {'ans': True,
                            'desc': to_remove + ' is not a manager by ' + owner}

                else:
                    return {'ans': False,
                            'desc': to_remove + ' is not a appointed by ' + owner}
            else:
                return {'ans': False,
                        'desc': to_remove + ' is not a manager of this store'}
        else:
            logger.error("%s is not a store owner", owner)
            return {'ans': False,
                    'desc': owner + ' is not an owner of this store'}

    def __remove_owner_all_appointed(self, to_remove, publisher):

        if to_remove in self.store_owners:
            self.store_owners.remove(to_remove)
            # send notification to user to_remove.
            publisher.store_ownership_update(self.store_id, self.name, [to_remove])
        if to_remove in self.store_managers.keys():
            self.store_managers.pop(to_remove)
        if to_remove in self.appointed_by.keys():
            for own_or_man in self.appointed_by[to_remove]:
                self.__remove_owner_all_appointed(own_or_man, publisher)
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
            if manager in self.appointed_by.get(owner):
                if manager in self.store_managers.keys():
                    permission_function = getattr(Store, permission)
                    if permission_function not in self.store_managers.get(manager):
                        self.store_managers[manager].append(permission_function)
                        return {'ans': True,
                                'desc': permission + ' has been added to ' + manager}
                    else:
                        return {'ans': False,
                                'desc': manager + ' has already this permission'}

                else:
                    return {'ans': False,
                            'desc': manager + ' is not a manager'}

            else:
                return {'ans': False,
                        'desc': manager + ' not appointed by ' + owner}

        else:
            logger.error("%s is not a store owner", owner)
            return {'ans': False,
                    'desc': owner + ' is not an owner of this store'}

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
                    if manager in self.appointed_by[owner]:
                        permission_function = getattr(Store, permission)
                        if permission_function in self.store_managers.get(manager):
                            self.store_managers[manager].remove(permission_function)
                            return {'ans': True,
                                    'desc': permission + ' has been removed from ' + manager}

                        else:
                            return {'ans': False,
                                    'desc': manager + ' dont has this permission'}

                    else:
                        return {'ans': False,
                                'desc': manager + ' not appointed by ' + owner}
                else:
                    return {'ans': False,
                            'desc': manager + ' is not a manager'}

        else:
            logger.error("%s is not a store owner", owner)
            return {'ans': False,
                    'desc': owner + 'is not an owner of this store'}

    def appoint_manager(self, owner, to_appoint):
        """

        Args:
            owner: user that in the owners list
            to_appoint: user that should be appoint to manager

        Returns:

        """
        if owner in self.store_owners:
            if to_appoint not in self.store_managers.keys():
                self.store_managers[to_appoint] = [getattr(Store, "get_sales_history")]
                self.appointed_by[owner].append(to_appoint)
                return {'ans': True,
                        'desc': to_appoint + ' has become a manager'}
            else:
                return {'ans': False,
                        'desc': to_appoint + ' is already a manager'}
        else:
            logger.error("%s is not a store owner", owner)
            return {'ans': False,
                    'desc': to_appoint + ' is not an owner'}

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories,
                    key_words: [str], amount):
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
        if self.check_permission(user_name, getattr(Store, "add_product")):
            self.inventory.add_product(product_name,
                                       Product(product_name, product_price, product_categories, key_words, amount))
            return {'ans': True,
                    'desc': "Product has benn added"}
        else:
            logger.error("%s Don't have this permission", user_name)
            return {'ans': False,
                    'desc': "User don't have permission"}

    def search(self, search_term: str = "", categories = [], key_words = []) -> [Product]:
        """

        Args:
            search_term: part of the wanted product name
            categories: categories to search in
            key_words:
        Returns:
                list of products
        """
        result = []
        for product_name in self.inventory.get_products().keys():
            if search_term in product_name:
                result.append(self.inventory.get_products().get(product_name))

        if len(categories)>0:
            result = [product for product in result if any(category in product.categories for category in categories)]

        if len(key_words)>0:
            result = [product for product in result if any(key_word in product.key_words for key_word in key_words)]

        return result

    def buy_product(self, product_name, amount):
        return self.inventory.buy_product(product_name, amount)

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        if self.check_permission(user, getattr(Store, "get_sales_history")) or is_admin:
            return {'ans': True,
                    'sales': self.sales,
                    'desc': ''}
        return {'ans': False,
                'sales': [],
                'desc': 'User dont have the permission'}

    def update_product(self, user, product_name, attribute, updated):
        if self.check_permission(user, getattr(Store, "update_product")):
            return {'ans': self.inventory.update_product(product_name, attribute, updated),
                    'desc': 'updated'}
        logger.error("%s don't have this permission", user)
        return {'ans': False,
                'desc': user + " don't have this permission"}

    def add_new_sale(self, purchase: Purchase, publisher: Publisher):
        """

         Args:

             purchase: Holds the store products bought by the user
         Returns:
                 True if @new_sale was added to @self.sales list, else false
                 :param purchase:
                 :param publisher:
         """
        if purchase is not None:
            self.sales.append(purchase)
            # send notification to owners.
            publisher.purchase_update(self.store_id, self.name, self.store_owners)
            return {'ans': True,
                    'desc': 'sale has been added'}
        return {'ans': False,
                'desc': 'sale has not been added'}

    def check_permission(self, user, function):
        return user in self.store_owners or \
               (user in self.store_managers and function in self.store_managers.get(user))

    def get_store_products(self):
        return {'ans': True,
                'desc': self.inventory.get_products()}

    def remove_product(self, product_name, username):
        if self.is_owner(username) or self.check_permission(username, getattr(Store, "remove_product")):
            return {'ans': self.inventory.remove_product(product_name),
                    'desc': 'product removed'}
        return {'ans': False,
                'desc': username + ' do not have permission'}

    def add_visible_product_discount(self, permitted_username, discount: Discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, getattr(Store, "add_visible_discount_to_product")):
            self.discount_idx += 1
            discount.id = self.discount_idx
            self.discounts[self.discount_idx] = discount
            return {'ans': True,
                    'desc': 'visible discount has been added'}
        return {'ans': False,
                'desc': permitted_username + ' do not have this permission'}

    def add_conditional_discount_to_product(self, permitted_username, discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, getattr(Store, "add_conditional_discount_to_product")):
            self.discount_idx += 1
            discount.id = self.discount_idx
            self.discounts[self.discount_idx] = discount
            return {'ans': True,
                    'desc': 'conditional discount has been added'}
        return {'ans': False,
                'desc': permitted_username + ' do not have this permission'}

    def add_conditional_discount_to_store(self, permitted_username, discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, getattr(Store, "add_conditional_discount_to_store")):
            self.discount_idx += 1
            discount.id = self.discount_idx
            self.discounts[self.discount_idx] = discount
            return {'ans': True,
                    'desc': 'conditional discount has been added'}
        return {'ans': False,
                'desc': permitted_username + ' do not have this permission'}

    def add_composite_discount(self, permitted_username: str, discount: Discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, getattr(Store, "add_composite_discount")):
            self.discount_idx += 1
            discount.id = self.discount_idx
            self.discounts[self.discount_idx] = discount
            return {'ans': True,
                    'desc': 'composite discount has been added'}
        return {'ans': False,
                'desc': permitted_username + ' do not have this permission'}

    def edit_visible_discount(self, permitted_username, discount_id, start_date,
                              end_date, percent):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username,
                                                                      getattr(Store, "edit_visible_discount")):
            discount = self.discounts[discount_id]
            return {'ans': discount.edit_discount(start_date, end_date, percent),
                    'desc': ''}
        return {'ans': False,
                'desc': permitted_username + ' do not have this permission'}

    def edit_conditional_discount_to_product(self, permitted_username: str, discount_id: int, start_date, end_date,
                                  percent, min_amount: int, nums_to_apply: int):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username,
                                                                      getattr(Store, "edit_conditional_discount_to_product")):
            discount = self.discounts[discount_id]
            return {'ans': discount.edit_discount(discount_id, start_date, end_date, percent, min_amount, nums_to_apply),
                    'desc': ''}
        return {'ans': False,
                'desc': permitted_username + ' do not have this permission'}

    def edit_conditional_discount_to_store(self, permitted_username: str, discount_id: int, start_date, end_date,
                                  percent: int, min_price: int):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username,
                                                                      getattr(Store, "edit_conditional_discount_to_store")):
            discount: ConditionalStoreDiscount = self.discounts[discount_id]
            return discount.edit_discount(discount_id, start_date, end_date, percent, min_price)
        return False

    def is_owner(self, username):
        if username in self.store_owners:
            return True
        return False

    def get_updated_basket(self, basket: Basket):
        product_price_dict = {}
        for product in basket.products.values():
            print(product)
            product_price_dict[product[0].name] = (product[0], product[1], product[0].get_price_by_amount(product[1]), product[0].original_price * product[1])  #{product_name, (amount, updated_price)}

        for discount in self.discounts.values():
            discount.commit_discount(product_price_dict)

        return product_price_dict  # {product_name, (Product, amount, updated_price, original_price)}

    def add_product_to_discount(self, permitted_user: str, discount_id: int, product_name: str):
        is_permitted = self.is_owner(permitted_user) or self.check_permission(permitted_user,
                                                                      getattr(Store, "add_product_to_discount"))
        is_in_inventory = product_name in self.inventory.products.keys()
        discount: Discount = self.discounts[discount_id]
        if is_permitted and is_in_inventory:
            discount.add_product(product_name)
            return {'ans': True,
                    'desc': 'product has been added to discount'}
        return {'ans': False,
                'desc': permitted_user + ' do not has this permission'}

    def remove_product_from_discount(self, permitted_user, discount_id, product_name):
        is_permitted = self.is_owner(permitted_user) or self.check_permission(permitted_user,
                                                                      getattr(Store, "remove_product_from_discount"))
        is_in_inventory = product_name in self.inventory.products.keys()
        discount: Discount = self.discounts[discount_id]
        if is_permitted and is_in_inventory:
            discount.remove_product(product_name)
            return {'ans': True,
                    'desc': 'product has been removed'}

        return {'ans': False,
                'desc': permitted_user + ' do not has this permission'}

    def add_purchase_store_policy(self, permitted_user, min_amount_products, max_amount_products):
        MAX_SIZE = 100000
        MIN_SIZE = 0

        if min_amount_products is None and max_amount_products is None:
            return {'ans': False, 'desc': "The parameters are not valid \n"}
        if not self.check_permission(permitted_user, getattr(Store, "add_purchase_store_policy")):
            return {'ans': False, 'desc': "User dont have permission\n"}

        min_amount = MIN_SIZE if min_amount_products is None else min_amount_products
        max_amount = MAX_SIZE if max_amount_products is None else max_amount_products
        self.purchases_idx += 1

        policy = PurchaseStorePolicy(min_amount, max_amount, self.purchases_idx)
        self.purchase_policies[self.purchases_idx] = policy

        return {'ans': True, 'desc': "Policy as been added"}

    def add_purchase_product_policy(self, permitted_user, min_amount_products, max_amount_products):
        MAX_SIZE = 100000
        MIN_SIZE = 0

        if min_amount_products is None and max_amount_products is None:
            return {'res': False, 'desc': "The parameters are not valid \n"}
        if not self.check_permission(permitted_user, getattr(Store, "add_purchase_product_policy")):
            return {'res': False, 'desc': "User dont have permission\n"}

        min_amount = MIN_SIZE if min_amount_products is None else min_amount_products
        max_amount = MAX_SIZE if max_amount_products is None else max_amount_products
        self.purchases_idx += 1

        policy = PurchaseProductPolicy(min_amount, max_amount, self.purchases_idx)
        self.purchase_policies[self.purchases_idx] = policy

        return {'ans': True, 'desc': "Policy as been added"}

    def add_purchase_composite_policy(self, permitted_user: str, policies: list, logic_operator: LogicOperator):
        if not self.check_permission(permitted_user, getattr(Store, "add_purchase_composite_policy")):
            return {'ans': False, 'desc': "User dont have permission\n"}

        self.purchases_idx += 1

        for policy in policies:
            del self.purchase_policies[policy.id]

        policy = PurchaseCompositePolicy(policies, logic_operator, self.purchases_idx)
        self.purchase_policies[self.purchases_idx] = policy

        return {'ans': True, 'desc': "Policy as been added"}

    def add_policy_to_purchase_composite_policy(self, permitted_user: str, composite_id, policy_id: int):
        if composite_id not in self.purchase_policies.keys() or policy_id not in self.purchase_policies.keys():
            return {'ans': False, 'desc': "One of the policies is not exist for this store"}

        if not self.check_permission(permitted_user, getattr(Store, "add_policy_to_purchase_composite_policy")):
            return {'ans': False, 'desc': "policy is not exist for this store\n"}

        self.purchase_policies[composite_id].add_policy(self.purchase_policies[policy_id])
        return {'ans': True, 'desc': "Policy as been added"}

    def add_product_to_purchase_product_policy(self, policy_id, permitted_user: str, product_name: str):
        if policy_id not in self.purchase_policies.keys():
            return {'ans': False, 'desc': "policy is not exist for this store\n"}

        if not self.check_permission(permitted_user, getattr(Store, "add_product_to_purchase_product_policy")):
            return {'ans': False, 'desc': "policy is not exist for this store\n"}

        self.purchase_policies[policy_id].add_product(product_name)
        return {'ans': True, 'desc': "Product has been added to policy"}

    def remove_product_from_purchase_product_policy(self, policy_id, permitted_user, product_name):
        if policy_id is None:
            return {'ans': False, 'desc': "No such policy"}
        if policy_id not in self.purchase_policies.keys():
            return {'ans': False, 'desc': "policy is not exist for this store\n"}
        if not self.check_permission(permitted_user,getattr(Store, "remove_product_from_purchase_product_policy")):
            return {'ans': False, 'desc': "User dont have permission\n"}
        self.purchase_policies[policy_id].remove_product(product_name)
        return {'ans': True, 'desc': product_name + " has been removed from policy \n"}

    def get_discounts(self):
        return {'ans': True,
                'desc': self.discounts}

    def get_discount_by_id(self, discount_id):
        if discount_id in self.discounts.keys():
            return {'ans': False, 'discount': self.discounts[discount_id]}

    def get_purchase_policies(self):
        return {'ans': True,
                'desc': self.purchase_policies}

    def get_purchase_policy_by_id(self, purchase_policy_id: int):
        if purchase_policy_id is None:
            return {'ans': False, 'desc': "No such policy"}

        if purchase_policy_id not in self.purchase_policies.keys():
            return {'ans': False, 'desc': "No such policy"}

        if purchase_policy_id in self.purchase_policies.keys():
            return {'ans': True, 'desc': self.purchase_policies[purchase_policy_id]}
            # return self.purchase_policies[purchase_policy_id]

    def check_basket_validity(self, basket: Basket):
        is_approved = True
        description = ""
        for policy in self.purchase_policies.values():
            p_approved, outcome = policy.is_approved(basket.products)
            if not p_approved:
                description += outcome
                is_approved = False

        return is_approved, description

    def remove_purchase_policy(self, policy_id, permitted_user):
        if policy_id is None or permitted_user is None:
            return {'ans': False, 'desc':  "The parameters are not valid \n"}

        if policy_id not in self.purchase_policies.keys():
            return {'ans': False, 'desc': "No such policy in this store \n"}

        del self.purchase_policies[policy_id]
        return {'ans': True, 'desc': "Policy has been removed \n"}

    def get_description(self):
        id = self.store_id
        inventory_description = self.get_inventory_description()
        discount_description = self.get_discounts()
        purchase_policies_description = self.get_purchase_policies()
        store_owners = self.store_owners
        store_managers = self.store_managers.keys()

        description = [id, inventory_description, discount_description,
                       purchase_policies_description, store_owners, store_managers]

        return description

    def get_inventory_description(self):
        return self.inventory

    # def get_jsn_description(self):
    #     return {"Store ID": self.store_id,
    #             "Name": self.name,
    #             "Inventory": self.inventory.get_jsn_description(),
    #             "Discounts": self.get_jsn_description_discounts(),
    #             "Purchase Policies": self.get_jsn_description_purchases(),
    #             "Store Owners": self.store_owners,
    #             "Store Managers": self.store_managers,
    #             "Sales": self.sales,
    #             "Rate": self.rate}

    # def get_jsn_description_discounts(self):
    #     discounts_description = []
    #     for discount in self.discounts.values():
    #         discounts_description.append(discount.get_jsn_description())
    #     return discounts_description

    # def get_jsn_description_purchases(self):
    #     policies_description = []
    #     for policy in self.purchase_policies.values():
    #         policies_description.append(policy.get_jsn_description())
    #     return policies_description

    def get_product(self, product_name):
        return self.inventory.get_product(product_name)

    def get_store_managers(self):
        store_managers_dict = {}
        for manager in self.store_managers.keys():
            store_managers_dict[manager] = []
            for perm in self.store_managers[manager]:
                store_managers_dict[manager].append(perm.__name__)
        return {'ans': True,
                'res': store_managers_dict}
