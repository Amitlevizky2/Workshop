from datetime import timedelta, datetime
from unittest import TestCase

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Discount import VisibleProductDiscount
from project.domain_layer.users_managment.UsersManager import UsersManager


class TestUsersManagerIntegration(TestCase):
    def setUp(self) -> None:
        self.users_manager = UsersManager()
        date_str = '04-10-2020'
        dt = timedelta(days=10)
        date_object = datetime.strptime(date_str, '%m-%d-%Y')
        self.product_orange = Product("orange", 2, "food", None, 100)
        self.product_orange.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_apple = Product("apple", 2, "food", None, 100)
        self.product_apple.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_petunia = Product("petunia", 5, "food", None, 100)
        self.product_petunia.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_begonia = Product("begonia", 15, "food", None, 100)
        self.product_begonia.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))

    # test register and assert that cart is transferred
    def test_register(self):
        guest_user_name = self.users_manager.add_guest_user()
        guest_cart = self.users_manager.get_cart(guest_user_name)
        self.assertTrue(self.users_manager.register(guest_user_name, "lielle", "12345"))
        self.assertEqual(guest_cart, self.users_manager.get_cart("lielle"))
        guest_user_name = self.users_manager.add_guest_user()
        self.assertFalse(self.users_manager.register(guest_user_name, "lielle", "12345"))

    def test_login(self):
        guest_user_name = self.users_manager.add_guest_user()
        self.users_manager.register(guest_user_name, "registered1", "7777777")
        registered1 = self.users_manager.find_reg_user("registered1")
        login_un = self.users_manager.login(guest_user_name, registered1.username, "7777777")
        self.assertEqual(self.users_manager.find_reg_user(login_un).loggedin, registered1.loggedin)

    def test_view_cart(self):
        pass

    def test_logout(self):
        pass

    def test_add_product(self):
        pass

    def test_remove_product(self):
        pass

    def test_add_managed_store(self):
        pass

    def test_add_purchase(self):
        pass

    def test_remove_cart(self):
        pass
