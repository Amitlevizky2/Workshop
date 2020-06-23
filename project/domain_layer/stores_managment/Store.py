from copy import deepcopy

from project.data_access_layer.StoreORM import StoreORM
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
    def __init__(self, store_id, name, store_owner, orm=None):
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
        if orm is None:
            self.orm = StoreORM()
            self.orm.id = store_id
            self.orm.name = name
            self.orm.discount_index = 0
            self.orm.appoint_owner(store_owner, "")
            self.orm.purchase_index = 0
            self.orm.add()
        else:
            self.orm = orm
        self.publisher = None

    def appoint_owner(self, owner, to_appoint, users_manager):
        """

        Args:
            owner:
            to_appoint:
            users_manager:
        Returns:

        """
        if owner in self.store_owners and \
                to_appoint not in self.store_owners:
            ans = self.appoint_owner_helper(owner, to_appoint, users_manager)
            if ans is False:
                return {'error': True,
                        'error_msg': 'User ' + to_appoint + ' does not exist.'}
            return {'error': False,
                    'data': 'appointed successfully.'}
        else:
            logger.error("%s is not a store owner or %s is already owner", owner, to_appoint)
            return {'error': True,
                    'error_msg': owner + "is not a store owner or " + to_appoint + " is already owner"}

    def appoint_owner_helper(self, owner, to_appoint, users_manager):
        self.store_owners.append(to_appoint)
        ans, message = users_manager.add_managed_store(to_appoint, self.store_id)
        if ans is False:
            return False
        print("**********************************")
        print("me:" + owner + " to_appoint " + to_appoint)
        # self.orm.appoint_owner(owner, to_appoint)
        self.appointed_by[to_appoint] = []
        if to_appoint in self.store_managers:
            self.store_managers.pop(to_appoint)
        self.appointed_by[owner].append(to_appoint)
        return True

    def remove_owner(self, owner, to_remove, publisher: Publisher, users_manager):

        """

        Args:
            owner:
            to_remove:
            :param users_manager:
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
                        self.__remove_owner_all_appointed(to_remove, publisher, users_manager)
                    # self.orm.remove_owner(to_remove)
                    return {'error': False,
                            'data': 'owner has been removed'}
                else:
                    logger.error("%s is not a store owner", owner)
                    return {'error': True,
                            'error_msg': to_remove + ' is not a appointed by ' + owner}
            else:
                return {'error': True,
                        'error_msg': to_remove + ' is not owner of this store'}
        else:
            return {'error': True,
                    'error_msg': to_remove + ' is not owner of this store'}

    def remove_manager(self, owner, to_remove, users_manager):

        """

        Args:
            owner:
            to_remove:
            users_manager:
        Returns:

        """
        if owner in self.store_owners:
            if to_remove in self.store_managers.keys():

                if to_remove in self.appointed_by.get(owner):

                    self.appointed_by[owner].remove(to_remove)
                    self.store_managers.pop(to_remove)
                    users_manager.remove_managed_store(to_remove, self.store_id)

                    return {'error': False,
                            'data': to_remove + ' is not a manager by ' + owner}

                else:
                    return {'error': True,
                            'error_msg': to_remove + ' is not a appointed by ' + owner}
            else:
                return {'error': True,
                        'error_msg': to_remove + ' is not a manager of this store'}
        else:
            logger.error("%s is not a store owner", owner)
            return {'error': True,
                    'error_msg': owner + ' is not an owner of this store'}

    def __remove_owner_all_appointed(self, to_remove, publisher, users_manager):

        if to_remove in self.appointed_by.keys():
            for own_or_man in self.appointed_by[to_remove]:
                self.__remove_owner_all_appointed(own_or_man, publisher, users_manager)
                print(own_or_man)
                print(to_remove)
            self.appointed_by.pop(to_remove)
        if to_remove in self.store_owners:
            self.store_owners.remove(to_remove)
            users_manager.remove_managed_store(to_remove, self.store_id)
            # send notification to user to_remove.
            publisher.store_ownership_update(self.store_id, self.name, [to_remove])
        if to_remove in self.store_managers.keys():
            self.store_managers.pop(to_remove)
            users_manager.remove_managed_store(to_remove, self.store_id)
        # publisher.store_ownership_update(self.store_id, self.name, [to_remove])

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
                    # permission_function = getattr(Store, permission)
                    if permission not in self.store_managers.get(manager):
                        self.store_managers[manager].append(permission)
                        self.orm.add_permission(manager, permission)
                        return {'error': False,
                                'data': permission + ' has been added to ' + manager}
                    else:
                        return {'error': True,
                                'error_msg': manager + ' has already this permission'}

                else:
                    return {'error': True,
                            'error_msg': manager + ' is not a manager'}

            else:
                return {'error': True,
                        'error_msg': manager + ' not appointed by ' + owner}

        else:
            logger.error("%s is not a store owner", owner)
            return {'error': True,
                    'error_msg': owner + ' is not an owner of this store'}

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
                    # permission_function = getattr(Store, permission)
                    if permission in self.store_managers.get(manager):
                        self.store_managers[manager].remove(permission)
                        self.orm.remove_permission(manager, permission)
                        return {'error': False,
                                'data': permission + ' has been removed from ' + manager}

                    else:
                        return {'error': True,
                                'error_msg': manager + ' dont has this permission'}

                else:
                    return {'error': True,
                            'error_msg': manager + ' not appointed by ' + owner}
            else:
                return {'error': False,
                        'error_msg': manager + ' is not a manager'}

        else:
            logger.error("%s is not a store owner", owner)
            return {'error': True,
                    'error_msg': owner + 'is not an owner of this store'}

    def appoint_manager(self, owner, to_appoint, users_manager):
        """

        Args:
            owner: user that in the owners list
            to_appoint: user that should be appoint to manager
            users_manager:
        Returns:

        """
        if owner in self.store_owners:
            if to_appoint not in self.store_managers.keys():
                self.store_managers[to_appoint] = ["view_purchase_history"]
                self.appointed_by[owner].append(to_appoint)
                answer = users_manager.add_managed_store(to_appoint, self.store_id)
                if answer is False:
                    return {'error': True,
                            'error_msg': 'User ' + to_appoint + ' does not exist.'}
                # self.orm.appoint_manager(owner, to_appoint)
                return {'error': False,
                        'data': to_appoint + ' has become a manager'}
            else:
                return {'error': True,
                        'error_msg': to_appoint + ' is already a manager'}
        else:
            logger.error("%s is not a store owner", owner)
            return {'error': True,
                    'error_msg': to_appoint + ' is not an owner'}

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
        if self.is_owner(user_name) or self.check_permission(user_name, 'update_products'):
            self.inventory.add_product(product_name,
                                       Product(product_name, product_price, product_categories, key_words, amount,
                                               self.store_id))
            return {'error': False,
                    'data': "Product has been added"}
        else:
            logger.error("%s Don't have this permission", user_name)
            return {'error': True,
                    'error_msg': "User don't have permission"}

    def search(self, search_term: str = "", categories=[], key_words=[]) -> [Product]:
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

        if len(categories) > 0:
            result = [product for product in result if any(category in product.categories for category in categories)]

        if len(key_words) > 0:
            result = [product for product in result if any(key_word in product.key_words for key_word in key_words)]

        result = deepcopy(result)
        self.products_after_discount(result)
        return result

    def products_after_discount(self, result):
        for product in result:
            for discount in self.discounts.values():
                product.original_price = discount.get_updated_price(product)

    def buy_product(self, product_name, amount):
        res = self.inventory.buy_product(product_name, amount)
        return res

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        if self.check_permission(user, 'view_purchase_history') or is_admin:
            # self.sales = self.orm.getPurchases()
            # TODO: fix purchase maybe handler maybe add function to store
            return {'error': False,
                    'data': self.sales}
        return {'error': True,
                'error_msg': 'User dont have the permission'}

    def update_product(self, user, product_name, new_price, new_amount):
        if self.check_permission(user, "update_products"):
            res1 = self.inventory.update_product(product_name, "original_price", new_price)
            res2 = self.inventory.update_product(product_name, "amount", new_amount)
            return {'error': not res1 and res2,
                    'data': 'updated'}
        logger.error("%s don't have this permission", user)
        return {'error': True,
                'error_msg': user + " don't have this permission"}

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
            return {'error': False,
                    'data': 'sale has been added'}
        return {'error': True,
                'error_msg': 'sale has not been added'}

    def check_permission(self, user, function):
        return user in self.store_owners or \
               (user in self.store_managers and function in self.store_managers.get(user))

    def get_store_products(self):
        return {'ans': True,
                'desc': self.inventory.get_products()}

    def remove_product(self, product_name, username):
        if self.is_owner(username) or self.check_permission(username, "update_products"):
            return {'error': not self.inventory.remove_product(product_name),
                    'data': 'product removed'}
        return {'error': True,
                'error_msg': username + ' do not have permission'}

    def add_visible_product_discount(self, permitted_username, discount: Discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, 'update_discounts'):
            self.discount_idx += 1
            discount.id = self.discount_idx
            self.discounts[self.discount_idx] = discount
            discount.set_id(self.discount_idx)
            return {'error': False,
                    'data': {'discount_id': self.discount_idx}}
        return {'error': True,
                'error_msg': permitted_username + ' do not have this permission'}

    def add_conditional_discount_to_product(self, permitted_username, discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, 'update_discounts'):
            self.discount_idx += 1
            discount.id = self.discount_idx
            self.discounts[self.discount_idx] = discount
            discount.set_id(self.discount_idx)
            return {'error': False,
                    'data':
                        {'discount_id': self.discount_idx}}
        return {'error': True,
                'error_msg': permitted_username + ' do not have this permission'}

    def add_conditional_discount_to_store(self, permitted_username, discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, 'update_discounts'):
            self.discount_idx += 1
            discount.id = self.discount_idx
            self.discounts[self.discount_idx] = discount
            discount.set_id(self.discount_idx)
            return {'error': False,
                    'data':
                        {'discount_id': self.discount_idx}}
        return {'error': True,
                'error_msg': permitted_username + ' do not have this permission'}

    def add_composite_discount(self, permitted_username: str, discount: Discount):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, 'update_discounts'):
            self.discount_idx += 1
            discount.id = self.discount_idx
            print("I'M OVER HERE")
            self.discounts[self.discount_idx] = discount
            discount.set_id(self.discount_idx)
            return {'error': False,
                    'data':
                        {'discount_id': self.discount_idx}}
        return {'error': True,
                'error_msg': permitted_username + ' do not have this permission'}

    def edit_visible_discount(self, permitted_username, discount_id, start_date,
                              end_date, percent, products=[]):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, 'update_discounts'):
            discount = self.discounts[discount_id]
            res = discount.edit_discount(start_date, end_date, percent, products)
            if res is True:
                return {'error': False,
                        'data': 'done'}
            return {'error': True, 'error_msg': 'Wrong edit information were given.'}
        return {'error': True,
                'error_msg': permitted_username + ' do not have this permission'}

    def edit_conditional_discount_to_product(self, permitted_username: str, discount_id: int, start_date, end_date,
                                             percent, min_amount: int, nums_to_apply: int, products=[]):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, 'update_discounts'):
            discount = self.discounts[discount_id]
            return {
                'error': not discount.edit_discount(discount_id, start_date, end_date, percent, min_amount,
                                                    nums_to_apply, products),
                'data': 'done'}
        return {'error': True,
                'error_msg': permitted_username + ' do not have this permission'}

    def edit_conditional_discount_to_store(self, permitted_username: str, discount_id: int, start_date, end_date,
                                           percent: int, min_price: int):
        if self.is_owner(permitted_username) or self.check_permission(permitted_username, 'update_discounts'):
            discount: ConditionalStoreDiscount = self.discounts[discount_id]
            return discount.edit_discount(discount_id, start_date, end_date, percent, min_price)
        return False

    def is_owner(self, username):
        if username in self.store_owners:
            return True
        return False

    def get_updated_basket(self, basket):
        product_price_dict = {}
        for product in basket.values():
            product_price_dict[product[0].name] = (product[0], product[1], product[0].get_price_by_amount(product[1]),
                                                   product[0].original_price * product[
                                                       1])  # {product_name, (amount, updated_price)}

        for discount in self.discounts.values():
            discount.commit_discount(product_price_dict)

        return product_price_dict  # {product_name, (Product, amount, updated_price, original_price)}

    def add_product_to_discount(self, permitted_user: str, discount_id: int, product_name: str):
        is_permitted = self.is_owner(permitted_user) or self.check_permission(permitted_user, 'update_discounts')
        is_in_inventory = product_name in self.inventory.products.keys()
        discount: Discount = self.discounts[discount_id]
        if is_permitted and is_in_inventory:
            discount.add_product(product_name)
            return {'error': False,
                    'data': 'product has been added to discount'}
        return {'error': True,
                'error_msg': permitted_user + ' do not has this permission'}

    def remove_product_from_discount(self, permitted_user, discount_id, product_name):
        is_permitted = self.is_owner(permitted_user) or self.check_permission(permitted_user, 'update_discounts')
        is_in_inventory = product_name in self.inventory.products.keys()
        discount: Discount = self.discounts[discount_id]
        if is_permitted and is_in_inventory:
            discount.remove_product(product_name)
            return {'error': False,
                    'data': 'product has been removed'}

        return {'error': True,
                'error_msg': permitted_user + ' do not has this permission'}

    def add_purchase_store_policy(self, permitted_user, min_amount_products, max_amount_products):
        MAX_SIZE = 100000
        MIN_SIZE = 0

        if min_amount_products is None and max_amount_products is None:
            return {'ans': False, 'desc': "The parameters are not valid \n"}
        if not self.check_permission(permitted_user, 'update_policy'):
            return {'ans': False, 'desc': "User dont have permission\n"}

        min_amount = MIN_SIZE if min_amount_products is None else min_amount_products
        max_amount = MAX_SIZE if max_amount_products is None else max_amount_products
        self.purchases_idx += 1
        print("GOT HERE MOTHERFUCKERRRRRRRRR")
        print("id is: " + str(self.purchases_idx))
        policy = PurchaseStorePolicy(min_amount, max_amount, self.purchases_idx, self.store_id)
        self.purchase_policies[self.purchases_idx] = policy
        # policy.set_id(self.purchases_idx)

        return {'error': False, 'data': "Policy as been added"}

    def add_purchase_product_policy(self, permitted_user, min_amount_products, max_amount_products):
        MAX_SIZE = 100000
        MIN_SIZE = 0

        if min_amount_products is None and max_amount_products is None:
            return {'error': True, 'error_msg': "The parameters are not valid \n"}
        if not self.check_permission(permitted_user, 'update_policy'):
            return {'error': True, 'error_msg': "User dont have permission\n"}

        min_amount = MIN_SIZE if min_amount_products is None else min_amount_products
        max_amount = MAX_SIZE if max_amount_products is None else max_amount_products
        self.purchases_idx += 1
        print("GOT HERE MOTHERFUCKERRRRRRRRR4")
        policy = PurchaseProductPolicy(min_amount, max_amount, self.purchases_idx, self.store_id)
        print("add_purchase_product_policy: policy")
        print(policy)
        self.purchase_policies[self.purchases_idx] = policy
        policy.set_id(self.purchases_idx)

        return {'error': False,
                'data': {'msg': "Policy as been added",
                         'policy_id': policy.id}}

    def add_purchase_composite_policy(self, permitted_user: str, policies: list, logic_operator: LogicOperator):
        if not self.check_permission(permitted_user, 'update_policy'):
            return {'error': True, 'error_msg': "User dont have permission\n"}

        self.purchases_idx += 1

        for policy in policies:
            print(policy.__dict__)
            del self.purchase_policies[policy.id]

        policy = PurchaseCompositePolicy(policies, logic_operator, self.purchases_idx, self.store_id)
        self.purchase_policies[self.purchases_idx] = policy
        policy.set_id(self.purchases_idx)

        return {'error': False, 'data': "Policy as been added"}

    def add_policy_to_purchase_composite_policy(self, permitted_user: str, composite_id, policy_id: int):
        if composite_id not in self.purchase_policies.keys() or policy_id not in self.purchase_policies.keys():
            return {'error': True, 'error_msg': "One of the policies is not exist for this store"}

        if not self.check_permission(permitted_user, 'update_policy'):
            return {'error': True, 'error_msg': "policy is not exist for this store\n"}

        self.purchase_policies[composite_id].add_policy(self.purchase_policies[policy_id])

        return {'error': False, 'data': "Policy as been added"}

    def add_product_to_purchase_product_policy(self, policy_id, permitted_user: str, product_name: str):
        if policy_id not in self.purchase_policies.keys():
            return {'error': True, 'error_msg': "policy is not exist for this store\n"}

        if not self.check_permission(permitted_user, 'update_policy'):
            return {'error': True, 'error_msg': "policy is not exist for this store\n"}

        self.purchase_policies[policy_id].add_product(product_name)
        return {'error': False, 'data': "Product has been added to policy"}

    def remove_product_from_purchase_product_policy(self, policy_id, permitted_user, product_name):
        if policy_id is None:
            return {'error': True, 'error_msg': "No such policy"}
        if policy_id not in self.purchase_policies.keys():
            return {'error': True, 'error_msg': "policy is not exist for this store\n"}
        if not self.check_permission(permitted_user, 'update_policy'):
            return {'error': True, 'error_msg': "User dont have permission\n"}
        self.purchase_policies[policy_id].remove_product(product_name)
        return {'error': False, 'data': product_name + " has been removed from policy \n"}

    def get_discounts(self):
        return {'ans': True,
                'desc': self.discounts}

    def get_discount_by_id(self, discount_id):
        if discount_id in self.discounts.keys():
            return {'error': False, 'discount': self.discounts[discount_id]}

    def get_purchase_policies(self):
        return self.purchase_policies

    def get_purchase_policy_by_id(self, purchase_policy_id: int):
        if purchase_policy_id is None:
            return {'ans': False, 'desc': "No such policy"}

        if purchase_policy_id not in self.purchase_policies.keys():
            return {'ans': False, 'desc': "No such policy"}

        if purchase_policy_id in self.purchase_policies.keys():
            return {'ans': True, 'desc': self.purchase_policies[purchase_policy_id]}
            # return self.purchase_policies[purchase_policy_id]

    def check_basket_validity(self, basket):
        is_approved = True
        description = ""
        for policy in self.purchase_policies.values():

            p_approved, outcome = policy.is_approved(basket)
            if not p_approved:
                description += outcome
                is_approved = False

        for product_name in basket.keys():
            valid = self.is_valid_amount(product_name, basket[product_name][1])
            if valid['error'] is True:
                description += valid['error_msg']
                is_approved = False

        return is_approved, description

    def remove_purchase_policy(self, policy_id, permitted_user):
        if policy_id is None or permitted_user is None:
            return {'error': True, 'error_msg': "The parameters are not valid \n"}

        if policy_id not in self.purchase_policies.keys():
            return {'error': False, 'error_msg': "No such policy in this store \n"}

        del self.purchase_policies[policy_id]
        return {'error': False, 'data': "Policy has been removed \n"}

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

    def get_product(self, product_name):
        return self.inventory.get_product(product_name)

    def get_store_managers(self):
        # store_managers_dict = {}
        # for manager in self.store_managers.keys():
        #     store_managers_dict[manager] = []
        #     for perm in self.store_managers[manager]:
        #         store_managers_dict[manager].append(perm)
        return {'error': False,
                'data': list(self.store_managers.keys())}

    def get_user_permissions(self, username):
        permissions = {'username': username}
        return_val = {}
        if username in self.store_owners:
            permissions['permissions'] = self.get_all_permissions()
            return_val['error'] = False
            return_val['data'] = permissions
        else:
            if username in self.store_managers.keys():
                permissions['permissions'] = self.store_managers[username]
                return_val['error'] = False
                return_val['data'] = permissions
            else:
                return_val['error'] = True
                return_val['error_msg'] = 'The user' + username + 'does not have any permissions.'
        return return_val

    def get_all_permissions(self):
        return [
            "update_products",
            "update_policy",
            "update_discounts",
            "edit_owners",
            "appoint_owner",
            "edit_managers",
            "apporint_managers",
            "view_purchase_history"]

    def is_valid_amount(self, product_name, quantity):
        return self.inventory.is_valid_amount(product_name, quantity)

    def edit_store_manager_permissions(self, owner, manager, new_permissions):
        manager_permissions = self.get_user_permissions(manager)
        if manager_permissions['error'] is True:
            return manager_permissions
        curr_permissions = set(manager_permissions['data']['permissions'])
        _new_permissions = set(new_permissions)
        print('curr_permissions: ')
        print(curr_permissions)
        print('_new_permissions: ')
        print(_new_permissions)
        add_permissions = set(_new_permissions - curr_permissions)
        print('add_permissions: ')
        print(add_permissions)
        remove_permissions = set(curr_permissions - _new_permissions)
        print('remove_permissions: ')
        print(remove_permissions)
        for new_permission in add_permissions:
            res = self.add_permission_to_manager(owner, manager, new_permission)
            if res['error'] is True:
                return res
        for remove_permission in remove_permissions:
            res = self.remove_permission_from_manager(owner, manager, remove_permission)
            if res['error'] is True:
                return res
        return {
            'error': False,
            'data': 'Permissions have been updated.'
        }

    def intersection(self, lst1, lst2):
        return list(set(lst1) & set(lst2))
