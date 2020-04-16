from unittest import TestCase

from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
from project.domain_layer.users_managment.User import User
from project.domain_layer.users_managment.UsersManager import UsersManager


class TestUserManager(TestCase):
    def setUp(self) -> None:
        self.users_mng = UsersManager()
        self.reg_user1 = RegisteredUser("reg_user1")

    def test_find_reg_user(self):
        self.users_mng.reg_user_list.pop("reg_user1")
        if "reg_user1" not in self.users_mng.reg_user_list.keys():
            self.users_mng.reg_user_list["reg_user1"] = self.reg_user1

        reg_user_test = self.users_mng.find_reg_user("reg_user1")
        self.assertEqual(reg_user_test, self.reg_user1)

    def test_find_user(self):
        self.fail()

    def test_register(self):
        self.fail()

    def test_login(self):
        self.users_mng.security.add_user("lielle", "noa")
        user = User("guestUser800")
        self.users_mng.guest_user_list[user.username] = user
        reg_lielle = RegisteredUser("lielle")
        self.users_mng.reg_user_list["lielle"] = reg_lielle

        login_un = self.users_mng.login("guestUser800", "lielle", "noa")
        self.assertEqual(login_un, "lielle")

        login_un = self.users_mng.login("guestUser800", "lielle", "not_noa")
        self.assertFalse(login_un)

        login_un = self.users_mng.login("guestUser800", "bla", "not_noa")
        self.assertFalse(login_un)

        self.users_mng.reg_user_list.pop("lielle")

    def test_add_guest_user(self):
        self.assertTrue("guestUser" + str(self.users_mng.incremental_id) not in self.users_mng.guest_user_list.keys())
        self.users_mng.add_guest_user()
        self.assertTrue("guestUser" + str(self.users_mng.incremental_id - 1) in self.users_mng.guest_user_list.keys())

    def test_view_cart(self):
        self.fail()

    def test_logout(self):
        reg_user10 = RegisteredUser("reg_user10")
        self.users_mng.reg_user_list["reg_user10"] = reg_user10
        reg_user10.loggedin = True
        logout_un = self.users_mng.logout("reg_user10")
        incr = self.users_mng.incremental_id - 1
        self.assertEqual(logout_un, "guestUser"+str(incr))

        logout_un2 = self.users_mng.logout("not_registered")
        self.assertEqual(logout_un2, "not_registered")

    def test_view_purchases(self):
        self.fail()

    def test_add_product(self):
        self.fail()

    def test_remove_product(self):
        self.fail()

    def test_get_cart(self):
        self.fail()

    def test_view_purchases_admin(self):
        self.fail()

    def test_is_admin(self):
        self.fail()

    def test_add_managed_store(self):
        self.fail()

    def test_get_managed_stores(self):
        self.fail()

    def test_check_if_registered(self):
        self.fail()

    def test_check_if_loggedin(self):
        self.fail()

    def test_add_purchase(self):
        self.fail()

    def test_remove_cart(self):
        self.fail()
