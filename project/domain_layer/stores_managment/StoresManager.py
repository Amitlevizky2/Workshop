import logging
from project import logger

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.CompositeDiscount import CompositeDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalProductDiscount import \
    ConditionalProductDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalStoreDiscount import ConditionalStoreDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import VisibleProductDiscount
from project.domain_layer.stores_managment.NullStore import NullStore
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.PurchasesPolicies import PurchasePolicy
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.users_managment import Basket
from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.communication_managment.Publisher import Publisher

import jsons

from project.domain_layer.users_managment.UsersManager import UsersManager


def get_logic_operator(logic_operator_str: str):
    if logic_operator_str is None:
        return None
    if logic_operator_str.upper() == "OR":
        return LogicOperator.OR
    elif logic_operator_str.upper() == "AND":
        return LogicOperator.AND
    elif logic_operator_str.upper() == "XOR":
        return LogicOperator.XOR
    else:
        return None


class StoresManager:
    def __init__(self, data_handler):
        self.publisher = None
        self.users_manager = None
        self.stores = {}
        self.stores_idx = 0
        self.data_handler = data_handler

    def update_product(self, store_id, user, product_name, new_price, new_amount):
        """
        Args:
            store_id: the store we want to update
            user: the user who wants to update
            product_name: product to update

        Returns:True if succeed
        :param user:
        :param product_name:
        :param store_id:
        :param new_price:

        """
        return jsons.dumps(self.get_store(store_id).update_product(user, product_name, new_price, new_amount))

    def search(self, search_term: str = "", categories=[], key_words=[]) -> {int: [Product]}:
        """

        Args:
            search_term: part of the wanted product name
            categories: categories to search in
            key_words:

        Returns:dist {Store:list of products in store}

        """
        search_result = {}
        for store_id in self.stores.keys():
            store = self.get_store(store_id)
            search_in_store = self.get_store(store_id).search(search_term, categories, key_words)
            if search_in_store is not None and len(search_in_store) > 0:
                search_result[store.name] = {'store_id': store_id,
                                             'search_res': search_in_store}
        return jsons.dumps(search_result)

    def get_store(self, store_id: int) -> Store:
        if store_id in self.stores.keys():
            print('ytdityetdndidify')
            return self.stores.get(store_id)
        else:
            if store_id is None:
                logger.error("store is none")
            else:
                logger.error("%d store id doesn't exist", store_id)
            return NullStore()

    def add_product_to_store(self, store_id: int, user_name: str, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount):
        """

        Args:
            amount:
            store_id:
            user_name:
            product_name:
            product_price:
            product_categories:
            key_words:

        Returns:

        """
        return jsons.dumps(self.get_store(store_id).add_product(user_name, product_name, product_price,
                                                                product_categories, key_words, amount))

    def appoint_manager_to_store(self, store_id, owner, to_appoint):
        """

        Args:
            store_id:
            owner:
            to_appoint:
        """
        return jsons.dumps(
            self.get_store(store_id).appoint_manager(owner, to_appoint, self.users_manager, self.publisher))

    def appoint_owner_to_store(self, store_id, owner, to_appoint):
        """

        Args:
            store_id:
            owner:
            to_appoint:
        """
        return jsons.dumps(
            self.get_store(store_id).appoint_owner(owner, to_appoint, self.users_manager, self.publisher))

    def add_permission_to_manager_in_store(self, store_id, owner, manager, permission: str):
        return jsons.dumps(
            self.get_store(store_id).add_permission_to_manager(owner, manager, permission, self.publisher))

    def remove_permission_from_manager_in_store(self, store_id, owner, manager, permission: str):
        return jsons.dumps(
            self.get_store(store_id).remove_permission_from_manager(owner, manager, permission, self.publisher))

    # TODO: add Publisher
    def add_purchase_to_store(self, store_id: int, purchase: Purchase):
        # send notification to user to_remove.
        store = self.get_store(store_id)
        return jsons.dumps(store.add_new_sale(purchase, self.publisher))

    # TODO: add publisher
    def open_store(self, owner: str, store_name):
        self.stores[self.stores_idx] = Store(self.stores_idx, store_name, owner)
        # send notification to user owner.
        # self.publisher.store_status_update(self.stores_idx, store_name, [owner], status='open')
        self.stores_idx += 1
        return self.stores_idx - 1

    def buy(self, cart: Cart):
        answer = jsons.loads(self.check_cart_validity(cart))
        print('STORE MANAGER')
        print(answer)
        if answer['error'] is True:
            print('STORE MANAGER')
            print('in if')
            return jsons.dumps({'error': True,
                                'error_msg': answer['description']})

        # # price, description =\
        # buy_res = jsons.loads(self.get_cart_description(cart))
        # price = buy_res['cart_price']
        # description = buy_res['cart_description']

        #  if user dont have enough money according to 'price' will return false

        #  user will also get a description for his purchase
        for store_id in cart.baskets.keys():
            basket = cart.get_basket(store_id)
            for product in basket.products.keys():
                print('store id is: {}'.format(str(store_id)))
                store = self.get_store(int(store_id)).buy_product(product, basket.products[product])
                if store['error'] is True:
                    print('in if')
                    return False

            # store_obj.sales.append(description[store_obj.name])
        return jsons.dumps({'error': False,
                            'data': 'confirmed'})

    def get_sales_history(self, store_id, user, is_admin):
        history = self.get_store(store_id).get_sales_history(user, is_admin)
        if history['error'] is False:
            if history['data'][0] is None:
                purcs = self.data_handler.find_store_purchases(store_id)
                if purcs[0] is None:
                    history['data'] = []
                    return history
                history['data'] = purcs
            history['data'] = []
        return jsons.dump(history)

    def get_store_products(self, store_id):
        return jsons.dumps(self.get_store(store_id).get_store_products())

    def remove_product_from_store(self, store_id, product_name, username):
        store = self.get_store(store_id)
        product = store.search(product_name)
        if product:
            return jsons.dumps(store.remove_product(product_name, username))
        return jsons.dumps(False)

    def add_visible_product_discount(self, store_id: int, username: str, start_date, end_date, percent: int, products):
        store = self.get_store(store_id)
        answer = store.add_visible_product_discount(username,
                                                    VisibleProductDiscount(start_date, end_date, percent, store_id))
        if start_date > end_date:
            return jsons.dumps({
                'error': True,
                'error_msg': 'Invalid Dates'
            })
        if answer['error'] is False:
            for product_name in products:
                self.add_product_to_discount(store_id, username, answer['data']['discount_id'], product_name)
        return jsons.dumps(answer)

    def add_conditional_discount_to_product(self, store_id: int, username: str, start_date, end_date, percent: int,
                                            min_amount: int, num_prods_to_apply: int, products: list):
        if start_date > end_date:
            return jsons.dumps({
                'error': True,
                'error_msg': 'Invalid Dates'
            })
        store = self.get_store(store_id)
        answer = store.add_conditional_discount_to_product(username, ConditionalProductDiscount(start_date, end_date,
                                                                                                percent, min_amount,
                                                                                                num_prods_to_apply,
                                                                                                store_id))
        if answer['error'] is False:
            for product_name in products:
                self.add_product_to_discount(store_id, username, answer['data']['discount_id'], product_name)
        return jsons.dumps(answer)

    def add_conditional_discount_to_store(self, store_id: int, username: str, start_date, end_date, percent: int,
                                          min_price: int):
        if start_date > end_date:
            return jsons.dumps({
                'error': True,
                'error_msg': 'Invalid Dates'
            })
        store = self.get_store(store_id)
        return jsons.dumps(store.add_conditional_discount_to_store(username,
                                                                   ConditionalStoreDiscount(start_date, end_date,
                                                                                            percent, min_price,
                                                                                            store_id)))

    def add_product_to_discount(self, store_id: int, permitted_user: str, discount_id: int, product_name):
        store = self.get_store(store_id)
        x = 6
        return store.add_product_to_discount(permitted_user, discount_id, product_name)

    def remove_product_from_discount(self, store_id: int, permitted_user: str, discount_id: int, product_name):
        store = self.get_store(store_id)
        return jsons.dumps(
            store.remove_product_from_discount(permitted_user, discount_id, product_name))

    def add_composite_discount(self, store_id: int, username: str, start_date, end_date, logic_operator_str: str,
                               discounts_products_dict: dict, discounts_to_apply_id: list):
        if start_date > end_date:
            return jsons.dumps({
                'error': True,
                'error_msg': 'Invalid Dates'
            })
        store = self.get_store(store_id)  # {dicount_id, [product_names]}
        tup_list = []
        discounts_to_apply_list = []
        logic_operator: LogicOperator = get_logic_operator(logic_operator_str)

        for discount_id in discounts_products_dict.keys():
            if discount_id not in store.discounts.keys():
                return jsons.dumps(False)
            discount: Discount = store.discounts[discount_id]
            products_to_check_list = discounts_products_dict[discount_id]
            tup_list.append((discount, products_to_check_list))  # (Discount, (products_names))

        for discount_id in discounts_to_apply_id:
            if discount_id not in store.discounts.keys():
                return jsons.dumps(False)
            discount = store.discounts[discount_id]
            discounts_to_apply_list.append(discount)
            del store.discounts[discount_id]

        return jsons.dumps(store.add_composite_discount(username,
                                                        CompositeDiscount(start_date, end_date, logic_operator,
                                                                          tup_list, discounts_to_apply_list, store_id)))

    def edit_visible_discount_to_products(self, store_id: int, username: str, discount_id: int, start_date, end_date,
                                          percent: int, products=[]):
        store = self.get_store(store_id)
        return jsons.dumps(
            store.edit_visible_discount(username, discount_id, start_date, end_date, percent, products))

    def edit_conditional_discount_to_product(self, store_id: int, discount_id: int, username: str, start_date, end_date,
                                             percent: int,
                                             min_amount: int, nums_to_apply: int, products=[]):
        store = self.get_store(store_id)
        return jsons.dumps(
            store.edit_conditional_discount_to_product(username, discount_id, start_date, end_date, percent, min_amount,
                                                       nums_to_apply, products))

    def edit_conditional_discount_to_store(self, store_id: int, discount_id: int, username: str, start_date, end_date,
                                           percent: int,
                                           min_price: int):
        store = self.get_store(store_id)
        return jsons.dumps(
            store.edit_conditional_discount_to_store(username, discount_id, start_date, end_date, percent, min_price))

    def remove_manager(self, store_id, owner, to_remove):
        store = self.get_store(store_id)
        return jsons.dumps(store.remove_manager(owner, to_remove, self.users_manager, self.publisher))

    def remove_owner(self, store_id, owner, to_remove):
        store = self.get_store(store_id)
        return jsons.dumps(store.remove_owner(owner, to_remove, self.publisher, self.users_manager))

    def add_purchase_store_policy(self, store_id: int, permitted_user: str, min_amount_products: int,
                                  max_amount_products: int):
        store = self.get_store(store_id)
        return jsons.dumps(
            store.add_purchase_store_policy(permitted_user, min_amount_products, max_amount_products))

    def add_purchase_product_policy(self, store_id: int, permitted_user: str, min_amount_products: int,
                                    max_amount_products: int, products: list):
        if min_amount_products is not None:
            min_amount_products = int(min_amount_products)
        if max_amount_products is not None:
            max_amount_products = int(max_amount_products)

        store = self.get_store(store_id)
        answer = store.add_purchase_product_policy(permitted_user, min_amount_products, max_amount_products)
        if answer['error'] is False:
            for product_name in products:
                store.add_product_to_purchase_product_policy(answer['data']['policy_id'], permitted_user, product_name)

        return jsons.dumps(answer)

    def add_purchase_composite_policy(self, store_id: int, permitted_user: str, purchase_policies_id,
                                      logic_operator_str: str):
        logic_operator = get_logic_operator(logic_operator_str)
        if purchase_policies_id is None or logic_operator is None:
            return jsons.dumps({'error': True, 'error_msg': "The parameters are not valid"})

        store = self.get_store(store_id)
        policies = []

        for purch_policy_id in purchase_policies_id:
            if purch_policy_id not in store.purchase_policies.keys():
                return jsons.dumps({'error': True, 'error_msg': "Wrong policy id was inserted \n"})
            policy: PurchasePolicy = store.purchase_policies[purch_policy_id]
            policies.append(policy)

        return jsons.dumps(
            store.add_purchase_composite_policy(permitted_user, policies, logic_operator))

    def add_policy_to_purchase_composite_policy(self, store_id: int, permitted_user: str, composite_id: int,
                                                policy_id: int):
        store = self.get_store(store_id)
        return jsons.dumps(
            store.add_policy_to_purchase_composite_policy(permitted_user, composite_id, policy_id))

    def add_product_to_purchase_product_policy(self, store_id: int, policy_id: int, permitted_user: str,
                                               product_name: str):
        store = self.get_store(store_id)
        return jsons.dumps(
            store.add_product_to_purchase_product_policy(policy_id, permitted_user, product_name))

    def remove_purchase_policy(self, store_id: int, permitted_user: str, policy_id):
        store = self.get_store(store_id)
        return jsons.dumps(store.remove_purchase_policy(policy_id, permitted_user))

    def remove_product_from_purchase_product_policy(self, store_id: int, policy_id: int, permitted_user: str,
                                                    product_name: str):
        store = self.get_store(store_id)
        return store.remove_product_from_purchase_product_policy(policy_id, permitted_user, product_name)

    def get_discounts(self, store_id):
        store = self.get_store(store_id)
        description = store.get_discounts()
        return jsons.dumps(description)

    def get_discount_details(self, store_id: int, discount_id: int):
        store = self.get_store(store_id)
        discount = store.get_discount_by_id(discount_id)
        return jsons.dumps(discount)

    def get_purchases_policies(self, store_id):
        store = self.get_store(store_id)
        policies = store.get_purchase_policies()
        return jsons.dump({'ans': True,
                           'policies': policies})

    def get_purchase_policy_by_id(self, store_id: int, purchase_policy_id: int):
        store = self.get_store(store_id)
        desc = store.get_purchase_policy_by_id(purchase_policy_id)
        return jsons.dumps(desc)

    def check_cart_validity(self, cart: Cart):
        baskets = cart.baskets

        is_approved = True
        description = ''

        for basket in baskets.values():
            store = self.get_store(basket.store_id)
            description = ''
            basket_dict = self.get_basket_dict_purchase(store.inventory, basket)
            p_approved, outcome = store.check_basket_validity(basket_dict)

            if not p_approved:
                description += store.name + '\n' + outcome + '\n\n'
                is_approved = False

        return jsons.dumps({'error': not is_approved,
                            'description': description})

    def get_cart_description(self, cart: Cart):
        baskets = cart.baskets
        cart_price = 0
        cart_discription_dict = {}

        for basket in baskets.values():
            store = self.get_store(basket.store_id)
            updated_dict_basket = self.get_updated_basket(basket)
            basket_price = self.get_total_basket_price(updated_dict_basket)
            cart_price += basket_price
            desc = (self.get_basket_description(updated_dict_basket.values()))

            to_delete = []
            for product in desc.keys():
                if 'Store Discount' in product:
                    to_delete.append(product)

            for product in to_delete:
                desc.pop(product)

            cart_discription_dict[store.name] = {'store_name': store.name,
                                                 'store_id': basket.store_id,
                                                 'store_purchase_price': basket_price,
                                                 'desc': desc}

        return jsons.dumps({'ans': True,
                            'cart_price': cart_price,
                            'cart_description': cart_discription_dict})

    def get_updated_basket(self, basket):
        store = self.get_store(basket.store_id)
        basket_dict = self.get_basket_dict_discount(store.inventory, basket)
        return store.get_updated_basket(basket_dict)  # {product_name, (Product, amount, updated_price, policy)}

    def get_total_basket_price(self, updated_basket_dict):
        price = 0.0
        for product in updated_basket_dict.values():
            price += float(product[2])
        return price

    def get_basket_description(self, product_tup_list):
        basket_dict = {}
        for product_tup in product_tup_list:
            basket_dict[product_tup[0].name] = {"amount": product_tup[1],
                                                "price_after_disc": product_tup[2],
                                                "original_price": product_tup[
                                                    3]}  # [product_tup[1], product_tup[2], product_tup[3]]
        return basket_dict

    def get_stores_description(self):
        stores_description = {}  # {store_name: [store_details]}
        for store in self.stores.values():
            stores_description[store.name] = store.get_description()
        return jsons.dumps({'error': False,
                            'data': stores_description})

    def get_inventory_description(self, store_id: int):
        store = self.get_store(store_id)
        return jsons.dumps({'ans': True,
                            'inventory': store.inventory})

    # def get_jsn_description(self, store_id):
    #     store = self.get_store(store_id)
    #     jsn_desc = jsons.dumps(store)
    #     return jsn_desc

    def bound_publisher(self, publisher: Publisher):
        self.publisher = publisher

    def set_users_manager(self, users_manager: UsersManager):
        self.users_manager = users_manager

    def get_product_from_store(self, store_id, product_name):
        store = self.get_store(store_id)
        product = store.get_product(product_name)
        return jsons.dumps({'ans': True,
                            'product': product})

    def get_store_managers(self, store_id: int):
        store = self.get_store(store_id)
        managers = store.get_store_managers()
        return jsons.dumps(managers)

    def get_store_owners(self, store_id: int):
        store = self.get_store(store_id)
        return jsons.dumps({'error': False,
                            'data': store.store_owners})

    def get_store_description_by_id(self, store_id):
        return self.get_store(store_id).get_jsn_description()

    def get_basket_dict(self, inventory, basket):
        products = basket.products
        products_dict = {}
        for product in products.keys():
            products_dict[product] = (
                inventory.products[product], (products[product], inventory.products[product].original_price))
        return products_dict

    def get_basket_dict_purchase(self, inventory, basket):
        products = basket.products
        products_dict = {}
        for product in products.keys():
            products_dict[product] = (inventory.products[product], products[product])
        return products_dict

    def get_basket_dict_discount(self, inventory, basket):
        products = basket.products
        products_dict = {}
        for product in products.keys():
            products_dict[product] = (inventory.products[product], products[product],
                                      products[product] * inventory.products[product].original_price,
                                      products[product] * inventory.products[product].original_price)
        return products_dict

    def get_user_permissions(self, store_id, username):
        store = self.get_store(store_id)
        answer = store.get_user_permissions(username)
        print(answer)
        return jsons.dumps(answer)

    def is_valid_amount(self, store_id, product_name, quantity):
        store = self.get_store(store_id)
        return store.is_valid_amount(product_name, quantity)

    def edit_store_manager_permissions(self, store_id, owner, manager, permissions):
        store = self.get_store(store_id)
        answer = store.edit_store_manager_permissions(owner, manager, permissions, self.publisher)
        print(answer)
        return jsons.dumps(answer)

    # {product_name, (Product, amount, updated_price, original_price)}

    def init_data(self):
        self.stores_idx = self.data_handler.get_store_index()
        stores = self.data_handler.get_all_stores()
        for store in stores:
            self.stores[store.store_id] = store


