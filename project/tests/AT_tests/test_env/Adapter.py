import jsons

from project.service_layer.PurchaseManager import PurchaseManager
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface
from project.tests.external_systems.test_PaymentSystem import external_paymentstub
from project.tests.external_systems.test_ShipmentSystemInterface import external_shipmentstub
from project.tests.domain_layer.stores_managment.Stubs.PublisherStub import PublisherStub

class Adapter:
    def __init__(self):
        self.users_manager_interface = UsersManagerInterface(None)
        self.store_manager_interface = StoresManagerInterface(self.users_manager_interface,None)
        self.store_manager_interface.bound_publisher(PublisherStub(None))
        self.users_manager_interface.user_manager.bound_publisher_and_stats(PublisherStub(None))
        self.users_manager_interface.set_stores_manager(self.store_manager_interface)
        self.purchase_manager = PurchaseManager(self.users_manager_interface, self.store_manager_interface)
        self.purchase_manager.set_external_payment(external_paymentstub())
        self.purchase_manager.set_external_shipment(external_shipmentstub())
        self.username = self.users_manager_interface.add_guest_user()

        print(self.username)

    def register(self, username, password):
        return self.users_manager_interface.register(self.username, username, password)

    def login(self, username, password):
        res = self.users_manager_interface.login(self.username, username, password)

        self.username = username
        return res

    def showProductStore(self, store):
        pass

    def add_product_to_Store(self, store_id, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount):
        return self.store_manager_interface.add_product_to_store(store_id, self.username, product_name, product_price,
                                                                 product_categories, key_words, amount)

    def searchProduct(self, product="", category=[], key_words=[]):
        return self.store_manager_interface.search_product(product, category, key_words)

    def Open_store(self, store_name):
        return self.store_manager_interface.open_store(self.username, store_name)

    def get_managed_stores(self):
        return self.users_manager_interface.get_managed_stores(self.username)

    def logout(self):
        res = self.users_manager_interface.logout(self.username)
        res = jsons.loads(res)
        if(not res['error']):
            self.username = res['data']
        return self.username

    def get_purchase_history(self):
        return self.users_manager_interface.view_purchases(self.username)

    def add_discount_to_product(self, store_id,  username, start_date, end_date, percent,product_name):
        return self.store_manager_interface.add_visible_discount_to_product(store_id,username,start_date,end_date,percent,product_name)

    def add_product(self, store_id, product, amount):
        return self.users_manager_interface.add_product(self.username, store_id, product, amount)

    def buy(self,CCnumber,CCmonth,CCyear,CCholder,CCccv,CCid,address,city,country,zip):
        return self.purchase_manager.buy(self.username,CCnumber,CCmonth,CCyear,CCholder,CCccv,CCid,address,city,country,zip)

    def remove_product_from_store(self, store_id, product_name):
        return self.store_manager_interface.remove_product(store_id, product_name, self.username)

    def update_product(self, store_id, product_name, att, updated):
        return self.store_manager_interface.update_product(store_id,self.username, product_name, att, updated)

    def add_new_store_owner(self, user, store_id):
        return self.store_manager_interface.appoint_owner_to_store(store_id, self.username, user)

    def add_permission(self, store_id, user, permission):
        return self.store_manager_interface.add_permission_to_manager_in_store(store_id, self.username, user,
                                                                               permission)

    def remove_store_manager(self, store_id, user):
        return self.store_manager_interface.remove_manager(store_id,self.username,user)

    def view_store_history(self, store_id):
        return self.store_manager_interface.get_sales_history(store_id, self.username)


    def add_new_store_manager(self, user, store_id):
        return self.store_manager_interface.appoint_manager_to_store(store_id, self.username, user)

    def add_purchase_product_policy(self, store_id, permitted_user, min_amount_products, max_amount_products, products):
        return self.store_manager_interface.add_purchase_product_policy(store_id, permitted_user, min_amount_products, max_amount_products, products)

    def bound_publisher(self, publisher):
        return self.store_manager_interface.bound_publisher(publisher)

    def add_purchase_store_policy(self,store_id, permitted_user, min_amount_products, max_amount_products):
        return self.store_manager_interface.add_purchase_store_policy(store_id,permitted_user, min_amount_products, max_amount_products)

    def add_visible_discount_to_product(self, store_id, username, start_date, end_date, percent, products):
        return self.store_manager_interface.add_visible_discount_to_product(store_id,username,start_date,end_date,percent,products)

    def add_conditional_discount_to_store(self, store_id, username, start_date, end_date, percent, min_price):
        return self.store_manager_interface.add_conditional_discount_to_store(store_id,username,start_date,end_date,percent,min_price)

    def add_composite_discount(self, store_id, username, start_date, end_date, logic_operator, discounts_products_dict,
                               discounts_to_apply_id):
        return self.store_manager_interface.add_composite_discount(store_id,username,start_date,end_date,logic_operator,discounts_products_dict,discounts_to_apply_id)