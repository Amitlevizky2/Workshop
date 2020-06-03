import jsons

from project.domain_layer.stores_managment import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.users_managment import Cart


class StoresGetters:
    def __init__(self, stores_manager: StoresManager):
        self.stores_manager = stores_manager

    def get_stores_description(self):
        stores_description = {}  # {store_name: [store_details]}
        for store in self.stores_manager.stores.values():
            stores_description[store.name] = store
        return jsons.dumps({'ans': True,
                            'stores_description': stores_description})

    def get_store_description(self, store_id: int):
        store: Store = self.stores_manager.get_store(store_id)
        return jsons.dump({'ans': True,
                           'desc': store})

    def get_store_discounts(self, permitted_user: str, store_id: int):
        store = self.stores_manager.get_store(store_id)
        description = store.get_discounts()
        return jsons.dumps(description)

    def get_store_discount(self, permitted_user: str, store_id: int, discount_id: int):
        store = self.stores_manager.get_store(store_id)
        discount = store.get_discount_by_id(discount_id)
        return jsons.dumps(discount)

    def get_purchases_policies(self, permitted_user: str, store_id: int):
        store = self.stores_manager.get_store(store_id)
        policies = store.get_purchase_policies()
        return jsons.dump({'ans': True,
                           'policies': policies})

    def get_purchase_policy(self, permitted_user: str, store_id: int, purchase_policy_id: int):
        store = self.stores_manager.get_store(store_id)
        desc = store.get_purchase_policy_by_id(purchase_policy_id)
        return jsons.dumps(desc)

    def get_sales_history(self, permitted_user: str, store_id, user, is_admin):
        return jsons.dump(
            self.stores_manager.get_store(store_id).get_sales_history(user, is_admin))

    def get_store_products(self, permitted_user: str, store_id: int):
        return jsons.dumps(self.stores_manager.get_store(store_id).get_store_products())

    def get_cart_description(self, cart: Cart):
        baskets = cart.baskets
        cart_price = 0
        cart_discription_dict = {}

        for basket in baskets.values():
            store = self.stores_manager.get_store(basket.store_id)
            updated_dict_basket = self.stores_manager.get_updated_basket(basket)
            cart_price += self.stores_manager.get_total_basket_price(updated_dict_basket)
            cart_discription_dict[store.name] = (self.stores_manager.get_basket_description(updated_dict_basket.values()))

        return jsons.dumps({'ans': True,
                           'cart_price': cart_price,
                           'cart_description': cart_discription_dict})

    def get_basket_description(self, permitted_user: str, product_tup_list):
        basket_dict = {}
        for product_tup in product_tup_list:
            basket_dict[product_tup[0].name] = {"amount": product_tup[1],
                                                "price_after_disc": product_tup[2],
                                                "original_price": product_tup[3]}  #[product_tup[1], product_tup[2], product_tup[3]]
        return jsons.dumps(basket_dict)

    def get_inventory_description(self, permitted_user: str, store_id: int):
        store = self.stores_manager.get_store(store_id)
        return jsons.dumps({'ans': True,
                            'inventory': store.inventory})

    def get_product_from_store(self, permitted_user: str, store_id, product_name):
        store = self.stores_manager.get_store(store_id)
        product = store.get_product(product_name)
        return jsons.dumps({'ans': True,
                            'product': product})

    def get_store_managers(self, permitted_user: str, store_id: int):
        store = self.stores_manager.get_store(store_id)
        managers = store.get_store_managers()
        return jsons.dumps(managers)

    def get_store_owners(self, permitted_user: str, store_id: int):
        store = self.stores_manager.get_store(store_id)
        return jsons.dumps({'ans': True,
                            'store_owners': store.store_owners})
