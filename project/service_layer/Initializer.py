import time

from project.data_access_layer.Handler import Handler
from project.domain_layer.communication_managment.Publisher import Publisher
from project.service_layer.PurchaseManager import PurchaseManager
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface
from os import path
from project.data_access_layer import engine


class Initializer:
    def __init__(self, sio):
        self.data_handler = Handler()
        self.users_manager = UsersManagerInterface(self.data_handler)
        self.stores_manager = StoresManagerInterface(self.users_manager, self.data_handler)
        self.purchase_manager = PurchaseManager(self.users_manager, self.stores_manager)
        self.publisher = Publisher(sio)
        self.users_manager.set_stores_manager(self.stores_manager)
        self.stores_manager.bound_publisher(self.publisher)
        self.bound_managers()

        if path.exists("init.txt") and not engine.dialect.has_table(engine, "regusers"):
           # self.data_handler.init_db()
            file1 = open('init.txt', 'r')
            Lines = file1.readlines()
            sid = 0
            for line in Lines:
                ret = eval(line)
                if ret is not None:
                    sid = ret

            # print(self.stores_manager.stores_manager.get_store(0).store_managers)
        else:
            self.users_manager.init_data()
            self.stores_manager.init_data()
            # file1 = open('init.txt', 'w')
            # L = ""
            # for i in range(1, 7):
            #     L += "self.register(\"u" + str(i) + "\")\n"
            #
            # L += "self.open_store(\"u2\",\"s1\")\n"
            # L += "self.add_product(\"u2\",sid,\"diapers\",30,20)\n"
            # L += "self.appoint_owner(\"u2\",sid,\"u3\")\n"
            #
            # L += "self.appoint_manager(\"u3\",sid,\"u5\")\n"
            # L += "self.add_permission(\"u3\",sid,\"u5\",\"add_product\")\n"
            # L += "self.appoint_manager(\"u3\",sid,\"u6\")\n"
            # file1.writelines(L)
            # file1.close()
        self.users_manager.add_first_admin()

    def get_users_manager_interface(self) -> UsersManagerInterface:
        return self.users_manager

    def get_stores_manager_interface(self) -> StoresManagerInterface:
        return self.stores_manager

    def get_purchase_manager_interface(self):
        return self.purchase_manager

    def bound_managers(self):
        users = self.users_manager.get_users_manager()
        stores = self.stores_manager.get_stores_manager()
        stores.set_users_manager(users)
        self.publisher.set_users_manager(users)

    def register(self, username):
        guest = self.users_manager.add_guest_user()
        self.users_manager.register(guest, username, "pass")

    def open_store(self, username, store_name):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        sid = self.stores_manager.open_store(username, store_name)
        self.users_manager.logout(username)
        return sid

    def add_product(self, username, storeid, pname, price, quatity):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        print(self.stores_manager.add_product_to_store((storeid), username, pname, price, [], [], quatity))
        self.users_manager.logout(username)

    def appoint_manager(self, username, storeid, appointed):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.appoint_manager_to_store((storeid), username, appointed)
        self.users_manager.logout(username)

    def appoint_owner(self, username, storeid, appointed):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.appoint_owner_to_store((storeid), username, appointed)
        self.users_manager.logout(username)

    def add_permission(self, username, store_id, manager, permission):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.add_permission_to_manager_in_store((store_id), username, manager, permission)
        self.users_manager.logout(username)

    def add_product_discount(self, username, store_id, start_date, end_date, percent, products):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        discount = self.stores_manager.add_visible_discount_to_product(store_id, username, start_date, end_date,
                                                                       percent, products)
        print(discount)
        self.users_manager.logout(username)

#checkkkkkk
    def add_conditional_discount_to_store(self, username, store_id, start_date, end_date, percent, min_price):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        discount = self.stores_manager.add_conditional_discount_to_store(store_id, username, start_date, end_date,
                                                                         percent, min_price)
        print(discount)
        self.users_manager.logout(username)

    def add_product_to_basket(self, username, store_id, product_name, quantity ):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.users_manager.add_product(username, store_id, product_name, quantity)
        self.users_manager.logout(username)

    def add_purchase_product_policy_to_store(self, username, store_id, min_amount_products, max_amount_products, products):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.add_purchase_product_policy(store_id, username, min_amount_products, max_amount_products, products)
        self.users_manager.logout(username)

    def add_purchase_store_policy(self, username, store_id, min_amount_products, max_amount_products):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")

        self.stores_manager.add_purchase_store_policy(store_id, username, min_amount_products, max_amount_products)
        self.users_manager.logout(username)

    def add_conditional_product_discount(self, username, store_id, start_date, end_date, percent, min_amount, num_prods_to_apply, products):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.add_conditional_discount_to_product(store_id, username, start_date, end_date, percent, min_amount, num_prods_to_apply, products)
        self.users_manager.logout(username)

    def add_composite_discount(self, store_id, username, start_date, end_date, logic_opr, discounts_preds, discounts_to_apply):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.add_composite_discount(store_id, username, start_date, end_date, logic_opr,
                                                   discounts_preds, discounts_to_apply)
        self.users_manager.logout(username)

    def add_composite_policy(self, store_id, username, logic_opr, policies):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.add_purchase_composite_policy(store_id, username, policies, logic_opr)
        self.users_manager.logout(username)

    def add_policy_to_purchase_composite_policy(self, store_id: int, username: str, composite_id: int,
                                                policy_id: int):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.add_policy_to_purchase_composite_policy(store_id, username, composite_id, policy_id)
        self.users_manager.logout(username)
