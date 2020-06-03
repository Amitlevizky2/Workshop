from project.domain_layer.communication_managment.Publisher import Publisher
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface
from os import path


class Initializer:
    def __init__(self):
        self.users_manager = UsersManagerInterface()
        self.stores_manager = StoresManagerInterface(self.users_manager)
        self.publisher = Publisher()
        self.users_manager.set_stores_manager(self.stores_manager)
        self.stores_manager.bound_publisher(self.publisher)
        if path.exists("init.txt"):
            file1 = open('init.txt', 'r')
            Lines = file1.readlines()
            sid = 0
            for line in Lines:
                ret = eval(line)
                if ret is not None:
                    sid = ret

            print(self.stores_manager.stores_manager.get_store(0).store_managers)
        else:
            file1 = open('init.txt', 'w')
            L = ""
            for i in range(1, 7):
                L += "self.register(\"u" + str(i) + "\")\n"

            L += "self.open_store(\"u2\",\"s1\")\n"
            L += "self.add_product(\"u2\",sid,\"diapers\",30,20)\n"
            L += "self.appoint_owner(\"u2\",sid,\"u3\")\n"

            L += "self.appoint_manager(\"u3\",sid,\"u5\")\n"
            L += "self.add_permission(\"u3\",sid,\"u5\",\"add_product\")\n"
            L += "self.appoint_manager(\"u3\",sid,\"u6\")\n"
            file1.writelines(L)
            file1.close()

    def get_users_manager_interface(self) -> UsersManagerInterface:
        return self.users_manager

    def get_stores_manager_interface(self) -> StoresManagerInterface:
        return self.stores_manager

    def bound_managers(self):
        users = self.users_manager.get_users_manager()
        stores = self.stores_manager.get_stores_manager()
        users.set_stores_manager(stores)
        stores.set_users_manager(users)

    def register(self, username):
        guest = self.users_manager.add_guest_user()
        self.users_manager.register(guest, username, "pass")

    def open_store(self, username, store_name):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        sid= self.stores_manager.open_store(username, store_name)
        self.users_manager.logout(username)
        return sid

    def add_product(self, username, storeid, pname, price, quatity):
        guest = self.users_manager.add_guest_user()
        self.users_manager.login(guest, username, "pass")
        self.stores_manager.add_product_to_store((storeid), username, pname, price, [], [], quatity)
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
