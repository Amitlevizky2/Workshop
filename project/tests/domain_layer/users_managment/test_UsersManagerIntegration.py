from datetime import timedelta
import datetime
from unittest import TestCase


from project.domain_layer.stores_managment.Discounts.VisibleProductDiscount import VisibleProductDiscount
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.users_managment.Basket import Basket
from project.domain_layer.users_managment.UsersManager import UsersManager


class TestUsersManagerIntegration(TestCase):
    def setUp(self) -> None:
        self.users_manager = UsersManager()
        date_str = '04-10-2020'
        dt = timedelta(days=10)
        date_object = datetime.datetime(2020, 4, 10)
        self.product_orange = Product("orange", 2, "food", None, 100)
        self.product_orange.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_apple = Product("apple", 2, "food", None, 100)
        self.product_apple.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_petunia = Product("petunia", 5, "food", None, 100)
        self.product_petunia.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_begonia = Product("begonia", 15, "food", None, 100)
        self.product_begonia.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))

        ###############################################
        self.store_manager = StoresManager()
        self.guest_user = self.users_manager.add_guest_user()
        self.idx = 0

        self.store_id1 = self.users_manager.store_manager.open_store("test store1", "test owner1")
        self.store_id2 = self.users_manager.store_manager.open_store("test store2", "test owner2")
        self.store_id3 = self.users_manager.store_manager.open_store("test store3", "test owner3")
        self.store_id4 = self.users_manager.store_manager.open_store("test store4", "test owner4")

        self.products = {
            "Apple": Product("Apple", 20, ["Food"], ["Fruits"], 10),
            "Banana": Product("Banana", 20, ["Food"], ["Fruits"], 10),
            "Orange": Product("Orange", 20, ["Food"], ["Fruits"], 10),
            "Tomato": Product("Tomato", 20, ["Food"], ["Vegetables"], 10),
            "Cucumber": Product("Cucumber", 20, ["Food"], ["Vegetables"], 10),
            "Carrot": Product("Carrot", 20, ["Food"], ["Vegetables"], 10),
            "Iphone": Product("Iphone", 20, ["Electronics"], ["Computers"], 10),
            "Hard Disk": Product("Hard Disk", 20, ["Electronics"], ["Computers"], 10),
            "Keyboard": Product("Keyboard", 20, ["Electronics"], ["Computers"], 10)}

        self.users_manager.store_manager.get_store(self.store_id1).inventory.products = self.products
        self.users_manager.store_manager.get_store(self.store_id2).inventory.products = self.products
        self.users_manager.store_manager.get_store(self.store_id3).inventory.products = self.products
        self.users_manager.store_manager.get_store(self.store_id4).inventory.products = self.products

        self.discount = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 10)
        self.discount1 = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 30)

        self.users_manager.store_manager.get_store(self.store_id1).discounts[self.discount.id] = self.discount
        self.users_manager.store_manager.get_store(self.store_id1).discounts[self.discount1.id] = self.discount1
        self.users_manager.store_manager.get_store(self.store_id2).discounts[self.discount.id] = self.discount
        self.users_manager.store_manager.get_store(self.store_id3).discounts[self.discount1.id] = self.discount1

        self.discount.products_in_discount["Apple"] = self.users_manager.store_manager.get_store(self.store_id1).inventory.products[
            "Apple"]
        self.discount.products_in_discount["Tomato"] = self.users_manager.store_manager.get_store(self.store_id1).inventory.products[
            "Tomato"]
        self.discount1.products_in_discount["Apple"] = self.users_manager.store_manager.get_store(self.store_id1).inventory.products[
            "Apple"]
        self.discount.products_in_discount["Carrot"] = self.users_manager.store_manager.get_store(self.store_id1).inventory.products[
            "Carrot"]
        self.discount.products_in_discount["Keyboard"] = self.users_manager.store_manager.get_store(self.store_id1).inventory.products[
            "Keyboard"]
        self.discount.products_in_discount["Apple"] = self.users_manager.store_manager.get_store(self.store_id2).inventory.products[
            "Apple"]
        self.discount.products_in_discount["Tomato"] = self.users_manager.store_manager.get_store(self.store_id2).inventory.products[
            "Tomato"]
        self.discount.products_in_discount["Carrot"] = self.users_manager.store_manager.get_store(self.store_id2).inventory.products[
            "Carrot"]
        self.discount.products_in_discount["Keyboard"] = self.users_manager.store_manager.get_store(self.store_id2).inventory.products[
            "Keyboard"]
        self.discount.products_in_discount["Apple"] = self.users_manager.store_manager.get_store(self.store_id3).inventory.products[
            "Apple"]
        self.discount.products_in_discount["Tomato"] = self.users_manager.store_manager.get_store(self.store_id3).inventory.products[
            "Tomato"]
        self.discount1.products_in_discount["Apple"] = self.users_manager.store_manager.get_store(self.store_id3).inventory.products[
            "Apple"]
        self.discount.products_in_discount["Carrot"] = self.users_manager.store_manager.get_store(self.store_id3).inventory.products[
            "Carrot"]
        self.discount.products_in_discount["Keyboard"] = self.users_manager.store_manager.get_store(self.store_id3).inventory.products[
            "Keyboard"]

        self.basket1 = Basket(self.users_manager.store_manager.get_store(self.store_id1).store_id)
        self.basket2 = Basket(self.users_manager.store_manager.get_store(self.store_id2).store_id)
        self.basket3 = Basket(self.users_manager.store_manager.get_store(self.store_id3).store_id)

        self.basket1.products["Apple"] = (self.users_manager.store_manager.get_store(self.store_id1).inventory.products["Apple"], 10)
        self.basket1.products["Keyboard"] = (
            self.users_manager.store_manager.get_store(self.store_id1).inventory.products["Keyboard"], 5)
        self.basket1.products["Carrot"] = (self.users_manager.store_manager.get_store(self.store_id1).inventory.products["Carrot"], 1)
        self.basket2.products["Apple"] = (self.users_manager.store_manager.get_store(self.store_id2).inventory.products["Apple"], 3)
        self.basket2.products["Keyboard"] = (
            self.users_manager.store_manager.get_store(self.store_id2).inventory.products["Keyboard"], 7)
        self.basket2.products["Carrot"] = (self.users_manager.store_manager.get_store(self.store_id2).inventory.products["Carrot"], 5)
        self.basket3.products["Apple"] = (self.users_manager.store_manager.get_store(self.store_id3).inventory.products["Apple"], 5)
        self.basket3.products["Keyboard"] = (
            self.users_manager.store_manager.get_store(self.store_id3).inventory.products["Keyboard"], 5)
        self.basket3.products["Carrot"] = (self.users_manager.store_manager.get_store(self.store_id3).inventory.products["Carrot"], 2)

        self.cart = self.users_manager.get_cart(self.guest_user)
        self.cart.baskets[self.store_id1] = self.basket1
        self.cart.baskets[self.store_id2] = self.basket2
        self.cart.baskets[self.store_id3] = self.basket3
        ###################################################



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

    def test_view_cart_after_discount(self):
        self.cart_after_discount = self.users_manager.view_cart_after_discount(self.guest_user)
        x=5

