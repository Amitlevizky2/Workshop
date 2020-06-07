from unittest import TestCase

import jsonpickle

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.users_managment.NullUser import NullUser
from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
from project.domain_layer.users_managment.User import User
from project.domain_layer.users_managment.UsersManager import UsersManager
from project.service_layer.Security import Security
from project.service_layer.UsersManagerInterface import UsersManagerInterface


class TestUserManager(TestCase):
    def setUp(self) -> None:
        self.admin = UsersManagerInterface()
        self.users_mng = self.admin.user_manager
        self.security = Security()

    def test_find_reg_user(self):
        reg_user1 = RegisteredUser("reg_user1")
        self.users_mng.reg_user_list["reg_user1"] = reg_user1
        answer, reg_user_test = self.users_mng.find_reg_user("reg_user1")
        self.assertTrue(answer)
        self.users_mng.reg_user_list.pop("reg_user1")

    def test_find_user(self):
        user = User("guestUser111")
        self.users_mng.guest_user_list[user.username] = user
        reg_user1 = RegisteredUser("reg_user1")
        self.users_mng.reg_user_list["reg_user1"] = reg_user1
        ans, user111 = self.users_mng.find_user("guestUser111")
        self.assertEqual(user, user111)
        ans, reg_u = self.users_mng.find_user("reg_user1")
        self.assertEqual(reg_user1, reg_u)
        self.users_mng.reg_user_list.pop("reg_user1")

    def test_register(self):
        user = User("guestUser700")
        self.users_mng.guest_user_list[user.username] = user

        self.users_mng.register("guestUser700", "user200")
        self.assertTrue("user200" in self.users_mng.reg_user_list.keys())
        self.users_mng.reg_user_list.pop("user200")

        reg_lielle = RegisteredUser("lielle")
        self.users_mng.reg_user_list["lielle"] = reg_lielle
        ans, mmm = self.users_mng.register("guestUser700", "lielle")
        self.assertFalse(ans)
        self.users_mng.reg_user_list.pop("lielle")

    # def test_login(self):
    #     self.security.add_user("lielle", "noa")
    #     user = User("guestUser800")
    #     self.users_mng.guest_user_list[user.username] = user
    #     reg_lielle = RegisteredUser("lielle")
    #     self.users_mng.reg_user_list["lielle"] = reg_lielle
    #
    #     login_un = self.users_mng.login("guestUser800", "lielle")
    #     self.assertEqual(login_un, "lielle")
    #
    #     login_un = self.users_mng.login("guestUser800", "lielle")
    #     self.assertFalse(login_un)
    #
    #     login_un = self.users_mng.login("guestUser800", "bla")
    #     self.assertFalse(login_un)
    #
    #     self.users_mng.reg_user_list.pop("lielle")

    def test_add_guest_user(self):
        self.assertTrue("guestUser" + str(self.users_mng.incremental_id) not in self.users_mng.guest_user_list.keys())
        self.users_mng.add_guest_user()
        self.assertTrue("guestUser" + str(self.users_mng.incremental_id - 1) in self.users_mng.guest_user_list.keys())

    def test_view_cart(self):
        pass

    # def test_logout(self):
    #     reg_user10 = RegisteredUser("reg_user10")
    #     self.users_mng.reg_user_list["reg_user10"] = reg_user10
    #     reg_user10.loggedin = True
    #     logout_un = self.users_mng.logout("reg_user10")
    #     incr = self.users_mng.incremental_id - 1
    #     self.assertEqual(logout_un, "guestUser" + str(incr))
    #
    #     logout_un2 = self.users_mng.logout("not_registered")
    #     self.assertEqual(logout_un2, "not_registered")
    #
    #     self.users_mng.reg_user_list.pop("reg_user10")

    # def test_view_purchases(self):
    #     # #24
    #     reg_lielle = RegisteredUser("lielle")
    #     self.users_mng.reg_user_list["lielle"] = reg_lielle
    #     product_orange = Product("orange", 2, "food", None, 100)
    #     purchase = Purchase([product_orange], "lielle", 1234, 1)
    #     reg_lielle.purchase_history.append(purchase)
    #     purch = [purchase]
    #
    #     x = self.users_mng.view_purchases("lielle")
    #     self.assertEqual(x[0].purchase_id, purch[0].purchase_id)
    #
    #     user = User("guestUser1212")
    #     self.users_mng.guest_user_list[user.username] = user
    #     user.purchase_history.append(purchase)
    #     self.assertEqual(jsonpickle.decode(self.users_mng.view_purchases("guestUser1212"))[0].purchase_id, purch[0].purchase_id)
    #
    #     self.users_mng.reg_user_list.pop("lielle")

    # tested in test_Cart and in test_Basket
    def test_add_product(self):
        pass

    # tested in test_Cart and in test_Basket
    def test_remove_product(self):
        pass

    def test_get_cart(self):
        pass

    def test_view_purchases_admin(self):
        reg_lielle = RegisteredUser("lielle")
        self.users_mng.reg_user_list["lielle"] = reg_lielle
        product_orange = Product("orange", 2, "food", None, 100)
        purchase = Purchase([product_orange], "lielle", 1234, 1)
        reg_lielle.purchase_history.append(purchase)
        purch = [purchase]

        x = jsonpickle.decode(self.users_mng.view_purchases_admin("lielle", "admin"))
        self.assertEqual(x[0].purchase_id, purch[0].purchase_id)

        y, p = self.users_mng.view_purchases_admin("lielle", "not_admin")
        self.assertFalse(y)

        self.users_mng.reg_user_list.pop("lielle")

    def test_is_admin(self):
        self.assertTrue(self.users_mng.is_admin("admin"))
        self.assertFalse(self.users_mng.is_admin("not_admin"))

        # tested in test_RegisteredUser

    def test_add_managed_store(self):
        pass

    def test_get_managed_stores(self):
        pass

    def test_check_if_registered(self):
        reg_user95 = RegisteredUser("reg_user95")
        self.users_mng.reg_user_list["reg_user95"] = reg_user95

        self.assertTrue(self.users_mng.check_if_registered("reg_user95"))
        self.assertFalse(self.users_mng.check_if_registered("not_registered_user"))

        self.users_mng.reg_user_list.pop("reg_user95")

    def test_check_if_loggedin(self):
        reg_user95 = RegisteredUser("reg_user95")
        self.users_mng.reg_user_list["reg_user95"] = reg_user95

        self.assertFalse(self.users_mng.check_if_loggedin("reg_user95"))
        reg_user95.loggedin = True
        self.assertTrue(self.users_mng.check_if_loggedin("reg_user95"))
        self.assertFalse(self.users_mng.check_if_loggedin("not_registered_user"))

        self.users_mng.reg_user_list.pop("reg_user95")

    # tested in test_User
    def test_add_purchase(self):
        pass

    def test_remove_cart(self):
        pass
