import unittest

from project.data_access_layer import Base, engine
from project.domain_layer.communication_managment.Publisher import Publisher
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.CompositeDiscount import CompositeDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalProductDiscount import \
    ConditionalProductDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import VisibleProductDiscount
from project.domain_layer.stores_managment.Product import Product

from project.domain_layer.stores_managment.Store import Store
import datetime
import jsons
import os

from project.domain_layer.users_managment.Basket import Basket
from project.domain_layer.users_managment.UsersManager import UsersManager
from project.tests.domain_layer.stores_managment.Stubs.UsersManagerStub import UsersManagerStub


class PublisherStub(Publisher):

    def store_ownership_update(self, sid, name, rem, update_type=''):
        pass

    def store_management_update(self, store_id, store_name, users: [str], update_type=''):
        pass

    def purchase_update(self, sid, name, owen):
        pass

    def notify(self, message, user):
        pass


class TestStore(unittest.TestCase):
    def setUp(self):
        self.publisher = PublisherStub(None)
        self.user_manager = UsersManagerStub()
        self.store = Store(0, "test store", "test owner")
        self.store.store_managers = {"Moshe": [],
                                     "Amit": ['add_product', 'update_products'],
                                     "Hadar": [],
                                     "Lielle": ['remove_product'],
                                     "Noa": ['add_visible_product_discount'],
                                     "Evgeny": ['update_products']}

        self.standard_users = ["Avishay",
                               "Alex",
                               "Ron"]

        self.store.inventory.products = {"Apple": Product("Apple", 20, ["Food"], ["Fruits"], 30, 1),
                                         "Banana": Product("Banana", 20, ["Food"], ["Fruits"], 10, 1),
                                         "Orange": Product("Orange", 20, ["Food"], ["Fruits"], 10, 1),
                                         "Tomato": Product("Tomato", 20, ["Food"], ["Vegetables"], 10, 1),
                                         "Cucumber": Product("Cucumber", 20, ["Food"], ["Vegetables"], 10, 1),
                                         "Carrot": Product("Carrot", 20, ["Food"], ["Vegetables"], 10, 1),
                                         "Iphone": Product("Iphone", 20, ["Electronics"], ["Computers"], 10, 1),
                                         "Hard Disk": Product("Hard Disk", 20, ["Electronics"], ["Computers"], 10, 1),
                                         "Keyboard": Product("Keyboard", 20, ["Electronics"], ["Computers"], 10, 1)}

        self.discount = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 1)
        self.discount1 = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 1)
        self.discount2 = ConditionalProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 2,
                                                    2, 1)
        self.discount3 = ConditionalProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 7,
                                                    1, 1)
        self.discount4 = ConditionalProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 6,
                                                    3, 1)

        self.discount5 = ConditionalProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 100,
                                                    3, 1, 1)

        self.tup_disc_prod_name_list = []
        self.tup_disc_prod_name_list.append((self.discount3, ["Apple", "Carrot", "Keyboard"]))
        self.tup_disc_prod_name_list.append((self.discount4, ["Apple", "Tomato"]))

        self.discount9 = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 30, 1)
        self.discount6 = CompositeDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
                                           LogicOperator.AND,
                                           self.tup_disc_prod_name_list, [self.discount, self.discount9], 1)

        self.discount7 = CompositeDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
                                           LogicOperator.OR,
                                           self.tup_disc_prod_name_list, [self.discount, self.discount9], 1)

        self.discount8 = CompositeDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
                                           LogicOperator.XOR,
                                           self.tup_disc_prod_name_list, [self.discount, self.discount9], 1)

        self.store.discounts[0] = self.discount
        self.store.discounts[1] = self.discount1
        self.store.discounts[2] = self.discount2
        self.store.discounts[3] = self.discount3
        self.store.discounts[4] = self.discount4
        self.store.discounts[5] = self.discount5
        self.store.discounts[6] = self.discount6
        self.store.discounts[7] = self.discount7
        self.store.discounts[8] = self.discount8

        self.discount.products_in_discount["Apple"] = self.store.inventory.products["Apple"]
        self.discount.products_in_discount["Tomato"] = self.store.inventory.products["Tomato"]
        self.discount.products_in_discount["Carrot"] = self.store.inventory.products["Carrot"]
        self.discount.products_in_discount["Keyboard"] = self.store.inventory.products["Keyboard"]
        self.discount.products_in_discount["Hard Disk"] = self.store.inventory.products["Hard Disk"]
        self.discount1.products_in_discount["Apple"] = self.store.inventory.products["Apple"]
        self.discount2.products_in_discount["Orange"] = self.store.inventory.products["Orange"]
        self.discount3.products_in_discount["Apple"] = self.store.inventory.products["Apple"]
        self.discount3.products_in_discount["Carrot"] = self.store.inventory.products["Carrot"]
        self.discount3.products_in_discount["Keyboard"] = self.store.inventory.products["Keyboard"]
        self.discount4.products_in_discount["Apple"] = self.store.inventory.products["Apple"]
        self.discount5.products_in_discount["Tomato"] = self.store.inventory.products["Tomato"]
        self.discount5.products_in_discount["Hard Disk"] = self.store.inventory.products["Hard Disk"]
        self.discount6.products_in_discount["Iphone"] = self.store.inventory.products["Iphone"]
        self.discount6.products_in_discount["Hard Disk"] = self.store.inventory.products["Hard Disk"]
        self.discount7.products_in_discount["Iphone"] = self.store.inventory.products["Iphone"]
        self.discount7.products_in_discount["Hard Disk"] = self.store.inventory.products["Hard Disk"]
        self.discount8.products_in_discount["Iphone"] = self.store.inventory.products["Iphone"]
        self.discount8.products_in_discount["Hard Disk"] = self.store.inventory.products["Hard Disk"]
        self.discount9.products_in_discount["Hard Disk"] = self.store.inventory.products["Hard Disk"]

        self.basket = Basket('Shai', self.store.store_id)
        self.basket.products["Apple"] = (self.store.inventory.products["Apple"], 10)
        self.basket.products["Keyboard"] = (self.store.inventory.products["Keyboard"], 5)
        self.basket.products["Carrot"] = (self.store.inventory.products["Carrot"], 1)
        self.basket.products["Orange"] = (self.store.inventory.products["Orange"], 3)
        self.basket.products["Tomato"] = (self.store.inventory.products["Tomato"], 4)

        self.basket1 = Basket('Shai', self.store.store_id + 1)
        self.basket1.products["Apple"] = (self.store.inventory.products["Apple"], 10)
        self.basket1.products["Keyboard"] = (self.store.inventory.products["Keyboard"], 10)
        self.basket1.products["Carrot"] = (self.store.inventory.products["Carrot"], 10)
        self.basket1.products["Banana"] = (self.store.inventory.products["Banana"], 10)
        self.basket1.products["Orange"] = (self.store.inventory.products["Orange"], 10)
        self.basket1.products["Cucumber"] = (self.store.inventory.products["Cucumber"], 10)
        self.basket1.products["Iphone"] = (self.store.inventory.products["Iphone"], 10)
        self.basket1.products["Hard Disk"] = (self.store.inventory.products["Hard Disk"], 10)
        self.basket1.products["Tomato"] = (self.store.inventory.products["Tomato"], 10)

    def test_appoint_owner_one(self):
        # There is no such owner
        res = self.store.appoint_owner("not test owner", "Moshe", self.user_manager, self.publisher)
        self.assertTrue(res['error'])
        # Valid appointment
        res = self.store.appoint_owner("test owner", "Moshe", self.user_manager, self.publisher)
        self.assertFalse(res['error'])
        # Moshe is already a store owner, should not e appointed again
        res = self.store.appoint_owner("test owner", "Moshe", self.user_manager, self.publisher)
        self.assertTrue(res['error'])
        # circle appointment is not allowed
        res = self.store.appoint_owner("moshe", "test owner", self.user_manager, self.publisher)
        self.assertTrue(res['error'])

    def test_appoint_owner_two(self):
        self.store.appoint_owner("test owner", "Moshe", self.user_manager, self.publisher)
        # to_appoint is already owner of the store
        res = self.store.appoint_owner("test owner", "test owner", self.user_manager, self.publisher)
        self.assertTrue(res['error'])
        # If Moshe was a manager, pull him out from that list
        self.assertNotIn("Moshe", self.store.store_managers)
        # Moshe become part of the owners list
        self.assertIn("Moshe", self.store.store_owners)
        # Validate that Moshe was appointed by test owner and now become his appointee
        self.assertIn("Moshe", self.store.appointed_by["test owner"])

    def test_remove_owner_one(self):
        users = [*self.store.store_managers]
        self.store.appoint_owner("test owner", "Moshe", self.user_manager, self.publisher)
        self.appoint_managers_to_owners(users)

        # owner is not really a store owner
        res = self.store.remove_owner("Sebastian", "Amit", PublisherStub(None), self.user_manager)
        self.assertTrue(res['error'])
        # to_remove is not a store owner
        res = self.store.remove_owner("Amit", "Sebastian", PublisherStub(None), self.user_manager)
        self.assertTrue(res['error'])
        # to_remove was not appointed by owner
        res = self.store.remove_owner("Amit", "Lielle", PublisherStub(None), self.user_manager)
        self.assertTrue(res['error'])

    def test_remove_owner_two(self):
        users = [*self.store.store_managers]
        self.store.appoint_owner("test owner", "Moshe", self.user_manager, self.publisher)
        self.appoint_managers_to_owners(users)

        # Check that all of the owner that was appoint by Moshe will are in the owners list
        for i in range(0, len(users)):
            self.assertIn(users[i], self.store.store_owners)

        # Check that every appointed owner is in the appointed by list of his appointee
        for i in range(0, len(users) - 1):
            self.assertIn(users[i + 1], self.store.appointed_by[users[i]])

        self.store.remove_owner("test owner", "Moshe", PublisherStub(None), self.user_manager)
        # self.store.store_owners.remove('Moshe')
        # Check that all of the owner that was appoint by Moshe will be deleted
        for i in range(0, len(users)):
            self.assertNotIn(users[i], self.store.store_owners)

    def test_remove_manager_one(self):
        self.store.appoint_owner("test owner", "Moshe", self.user_manager, self.publisher)
        self.store.appoint_manager("Moshe", "Hadar", self.user_manager, self.publisher)

        # Amit is not owner
        res = self.store.remove_manager("Amit", "Lielle", self.user_manager, self.publisher)
        self.assertTrue(res['error'])
        # Ron is not in store managers dictionary
        res = self.store.remove_manager("test owner", "Ron", self.user_manager, self.publisher)
        self.assertTrue(res['error'])
        # Hadar was not appointed by test owner
        res = self.store.remove_manager("test owner", "Hadar", self.user_manager, self.publisher)
        self.assertTrue(res['error'])

    def test_remove_manager_two(self):
        self.appoint_users_to_managers()
        # Check that 3 managers was added to managers dictionary
        for i in range(0, len(self.standard_users)):
            self.assertIn(self.standard_users[i], self.store.store_managers)

        # Avishay should be in the appointed by test owner list
        self.assertIn("Avishay", self.store.appointed_by["test owner"])
        # test owner and Avishay are valid parameters to the method
        res = self.store.remove_manager("test owner", "Avishay", self.user_manager, self.publisher)
        self.assertFalse(res['error'])
        # Avishay should not be in store's mangers list.
        self.assertNotIn("Avishay", self.store.store_managers)
        # Avishay should not be in the appointed by test owner list
        self.assertNotIn("Avishay", self.store.appointed_by["test owner"])

    def test_add_permission_to_manager_one(self):
        # Sebastian is not in store managers dictionary
        res = self.store.remove_manager("test store", "Sebastian", self.user_manager, self.publisher)
        self.assertTrue(res['error'])

        self.appoint_users_to_managers()
        # Check that 3 managers was added to managers dictionary
        for i in range(0, len(self.standard_users)):
            self.assertIn(self.standard_users[i], self.store.store_managers)

        # Amit is not owner
        res = self.store.add_permission_to_manager("Amit", "Lielle", "add_product", self.publisher)
        self.assertTrue(res['error'])

        # Sebastian is not manager
        res = self.store.add_permission_to_manager("test owner", "Sebastian", "add_product", self.publisher)
        self.assertTrue(res['error'])
        self.store.appointed_by["test owner"].append("Amit")
        # add_product is already in Amit permissions
        res = self.store.add_permission_to_manager("test owner", "Amit", "add_product", self.publisher)
        self.assertTrue(res['error'])

    def test_add_permission_to_manager_two(self):
        self.appoint_users_to_managers()
        # Check that 3 managers was added to managers dictionary
        for i in range(0, len(self.standard_users)):
            self.assertIn(self.standard_users[i], self.store.store_managers)

        # Valid parameters to the add permission method, Alex will get the add product permission
        res = self.store.add_permission_to_manager("test owner", "Alex", "add_product", self.publisher)
        self.assertFalse(res['error'])

        # Add product permission should now be in Alex's permissions
        self.assertIn('add_product', self.store.store_managers["Alex"])

    def test_remove_permission_from_manager_one(self):
        # Amit is not an owner
        res = self.store.remove_permission_from_manager("Amit", "Evgeny", "add_product", self.publisher)
        self.assertTrue(res['error'])

        # Ron is not a manager, mannnn, that's a bummer
        res = self.store.remove_permission_from_manager("test owner", "Ron", "add_product", self.publisher)
        self.assertTrue(res['error'])

        self.appoint_users_to_managers()
        # You know that Ron does not have that permission, don't you?!
        res = self.store.remove_permission_from_manager("test owner", "Ron", "add_product", self.publisher)
        self.assertTrue(res['error'])

    def test_remove_permission_from_manager_two(self):
        pass
        # res = self.store.remove_permission_from_manager("test owner", "Alex", "add_product")
        # self.assertTrue(res['error'])
        #
        # self.appoint_users_to_managers()
        # self.store.appoint_owner("test owner", "Moshe")
        # self.store.appoint_manager("test owner", "Avishay")
        # self.store.appoint_manager("Moshe", "Ron")
        # self.store.add_permission_to_manager("test owner", "Avishay", "add_product")
        #
        # # Don't be blind dude, I just added Avishay's permissions the add product permission
        # self.assertIn('add_product', self.store.store_managers["Avishay"])
        #
        # # Moshe, it is really not your business what permissions Avishay have, Let it go.
        # res = self.store.remove_permission_from_manager("Moshe", "Avishay", "add_product")
        # self.assertTrue(res['error'])
        #
        # res = self.store.remove_permission_from_manager("test owner", "Ron", "add_product")
        # self.assertTrue(res['error'])
        #
        # # Look Avishay, it's is not you, its me, I'm taking this permission from you, I'm sorry
        # res = self.store.remove_permission_from_manager("test owner", "Avishay", "add_product")
        # self.assertFalse(res['error'])
        #
        # # Just wanna make sure you don't hide from this permission again man
        # self.assertNotIn('add_product', self.store.store_managers["Avishay"])
        #
        # # Ok, last time I swear
        # res = self.store.remove_permission_from_manager("test owner", "Avishay", "add_product")
        # self.assertTrue(res['error'])
        #
        # res = self.store.remove_permission_from_manager("Alex", "Avishay", "add_product")
        # self.assertTrue(res['error'])

    def test_appoint_manager_one(self):
        # Well, Moshe  you are not an owner yet, so...
        res = self.store.appoint_manager("Moshe", "Alex", self.user_manager,self.publisher)
        self.assertTrue(res['error'])

        # Evgeny, you need to come back to earth and now!, you are already a manager man
        res = self.store.appoint_manager("test owner", "Evgeny", self.user_manager,self.publisher)
        self.assertTrue(res['error'])

    def test_appoint_manager_two(self):
        # Welcome Ron, a whole new world is waiting for
        res = self.store.appoint_manager("test owner", "Ron", self.user_manager,self.publisher)
        self.assertFalse(res['error'])

        # Yeah well i"ll check for you if you were added to the managers list, chill out man
        self.assertIn("Ron", self.store.store_managers.keys())

        # Ok, test owner is so annoying! he makes me check that its recorded that you were appointed by him
        self.assertIn("Ron", self.store.appointed_by["test owner"])

        # Now that you become a manager, let see if you can see the store sales history
        self.assertIn('view_purchase_history', self.store.store_managers["Ron"])

    def test_add_product_one(self):
        # Lielle you silly, you don't have the add product permission, moreover,
        res = self.store.add_product("Lielle", "Macbook", 25, "Food", "Fruits", 20)
        x = 5
        self.assertTrue(res['error'])
        # Sebastian is not one of the users in the system.
        res = self.store.add_product("Sebastian", "Macbook", 25, "Food", "Fruits", 20)
        self.assertTrue(res['error'])

    def test_add_product_two(self):
        p = Product("Macbook", 25, "Food", "Fruits", 20, 1)
        # Just checking that the product is not exist
        self.assertNotIn("Macbook", self.store.inventory.products)
        # Amitush, you have the permission to add product, use it!
        res = self.store.add_product("Amit", p.name, p.original_price, p.categories, p.key_words, p.amount)
        x = 5
        self.assertFalse(res['error'])
        # Let's see if you did it well
        self.assertIn("Macbook", self.store.inventory.products)

    def test_search(self):
        # Well let's see if you have an Apple dude
        self.assertIn("Apple", self.store.search("Apple")[0].name)
        # Now let's get some category
        fruits_vegs = [self.store.inventory.products["Apple"],
                       self.store.inventory.products["Banana"],
                       self.store.inventory.products["Orange"],
                       self.store.inventory.products["Tomato"],
                       self.store.inventory.products["Cucumber"],
                       self.store.inventory.products["Carrot"]]

        res_key_words = self.store.search(key_words=["Fruits", "Vegetables"])
        res_categoty = self.store.search(categories=["Food"])
        self.assertEqual(len(fruits_vegs), len(res_key_words))
        self.assertEqual(len(fruits_vegs), len(res_categoty))
        # No such category
        self.assertListEqual([], self.store.search(categories=["Kitchen"]))
        # No such keywords
        self.assertListEqual([], self.store.search(key_words=["Compil"]))
        # No such name
        self.assertListEqual([], self.store.search(search_term="Melon"))

    def test_update_product(self):
        # Lielle dont have the permission to update the product
        res = self.store.update_product("Lielle", "Apple", "amount", 8)
        self.assertTrue(res['error'])
        # Evgeny have the permission
        res = self.store.update_product("Evgeny", "Apple", "amount", 8)
        self.assertFalse(res['error'])
        # Owner can always do that
        res = self.store.update_product("test owner", "Apple", "amount", 8)
        self.assertFalse(res['error'])
        # You can also append discount to a product

    def test_add_new_sale(self):
        # Sale is None

        res = self.store.add_new_sale(Purchase(["Apple"], "Bon", self.store.store_id, 1, 1), PublisherStub(None))
        x = 5
        self.assertFalse(res['error'])
        # Valid new sale
        res = self.store.add_new_sale(Purchase(["Apple"], "Ron", self.store.store_id, 1, 1), PublisherStub(None))
        x = 5
        self.assertFalse(res['error'])

    # def test_buy_product(self):
    #     # The amount of the product you are asking to but is to big
    #     # self.assertFalse(self.store.buy_product("Apple", 30), "Store Cannot sell more than what it has")
    #     # The amount of the product is illegal
    #     res = self.store.buy_product("Apple", -1), "Store Cannot sell more than what it has"
    #     self.assertFalse(res['ans'])
    #     # Buying in good amount
    #     res = self.store.buy_product("Apple", 5), "This is a valid amount it should be ok!"
    #     self.assertTrue(res['ans'])

    # def test_remove_product(self):
    #     res = self.store.remove_product("Melon", "test owner")
    #     self.assertFalse(res['ans'])
    #     res = self.store.remove_product("Apple", "test owner")
    #     self.assertTrue(res['ans'])
    #     res = self.store.remove_product("Banana", "Ron")
    #     self.assertFalse(res['ans'])
    #     res = self.store.remove_product("Banana", "Lielle")
    #     self.assertTrue(res['ans'])

    # def test_basket_visible_discount(self):
    #     self.store.discounts[0] = self.discount
    #     self.store.discounts[5] = self.discount5
    #     view_cart_dict = self.store.get_updated_basket(self.basket)
    #     self.assertEqual(56, view_cart_dict["Tomato"][2])
    #
    # def test_basket_conditional_discount(self):
    #     self.store.discounts[2] = self.discount2
    #     self.basket2 = Basket(self.store.store_id)
    #     self.basket2.products["Orange"] = (self.store.inventory.products["Orange"], 4)
    #     cart2 = self.store.get_updated_basket(self.basket2)
    #     self.assertEqual(78, cart2["Orange"][2])
    #
    # def test_basket_and_Composite_discount(self):
    #     self.store.discounts[3] = self.discount3
    #     self.store.discounts[4] = self.discount4
    #     self.store.discounts[6] = self.discount6
    #     self.store.discounts[9] = self.discount9
    #     self.basket2 = Basket(self.store.store_id)
    #     self.basket2.products["Apple"] = (self.store.inventory.products["Apple"], 10)
    #     self.basket2.products["Carrot"] = (self.store.inventory.products["Carrot"], 10)
    #     self.basket2.products["Keyboard"] = (self.store.inventory.products["Keyboard"], 10)
    #     self.basket2.products["Tomato"] = (self.store.inventory.products["Tomato"], 10)
    #     self.basket2.products["Hard Disk"] = (self.store.inventory.products["Hard Disk"], 10)
    #     cart = self.store.get_updated_basket(self.basket2)
    #     self.assertEqual(140, cart["Hard Disk"][2])
    #
    # def test_basket_or_Composite_discount(self):
    #     self.store.discounts[3] = self.discount3
    #     self.store.discounts[4] = self.discount4
    #     self.store.discounts[7] = self.discount7
    #     self.store.discounts[9] = self.discount9
    #     self.basket2 = Basket(self.store.store_id)
    #     self.basket2.products["Apple"] = (self.store.inventory.products["Apple"], 10)
    #     #self.basket2.products["Carrot"] = (self.store.inventory.products["Carrot"], 10)
    #     self.basket2.products["Keyboard"] = (self.store.inventory.products["Keyboard"], 10)
    #     self.basket2.products["Tomato"] = (self.store.inventory.products["Tomato"], 10)
    #     self.basket2.products["Hard Disk"] = (self.store.inventory.products["Hard Disk"], 10)
    #     cart = self.store.get_updated_basket(self.basket2)
    #     self.assertEqual(140, cart["Hard Disk"][2])
    #
    # def test_basket_xor_Composite_discount(self):
    #     self.store.discounts[3] = self.discount3
    #     self.store.discounts[4] = self.discount4
    #     self.store.discounts[8] = self.discount8
    #     self.store.discounts[9] = self.discount9
    #     self.basket2 = Basket(self.store.store_id)
    #     self.basket2.products["Apple"] = (self.store.inventory.products["Apple"], 10)
    #     #self.basket2.products["Carrot"] = (self.store.inventory.products["Carrot"], 10)
    #     self.basket2.products["Keyboard"] = (self.store.inventory.products["Keyboard"], 10)
    #     self.basket2.products["Tomato"] = (self.store.inventory.products["Tomato"], 10)
    #     self.basket2.products["Hard Disk"] = (self.store.inventory.products["Hard Disk"], 10)
    #     cart = self.store.get_updated_basket(self.basket2)
    #     self.assertEqual(140, cart["Hard Disk"][2])R

    def appoint_managers_to_owners(self, users):
        for i in range(0, len(users) - 1):
            self.store.appoint_owner(users[i], users[i + 1], self.user_manager, PublisherStub(None))

    def appoint_users_to_managers(self):
        for i in range(0, len(self.standard_users)):
            self.store.appoint_manager("test owner", self.standard_users[i], self.user_manager, PublisherStub(None))

    # def test_remove_product_from_discount(self):
    #     self.discount2.id = 0
    #     self.store.discounts[0] = self.discount2
    #     view_cart_dict = self.store.get_updated_basket(self.basket)
    #     self.assertEqual(59, view_cart_dict["Orange"][2])
    #     self.store.remove_product_from_discount("test owner", self.discount2.id, "Orange")
    #     view_cart_dict = self.store.get_updated_basket(self.basket)
    #     self.assertEqual(60, view_cart_dict["Orange"][2])

    def tearDown(self) -> None:
        self.drop_table('stores')
        self.drop_table('baskets')
        self.drop_table('CompositeDiscounts')
        self.drop_table('CompositePolicies')
        self.drop_table('conditionalproductdiscounts')
        self.drop_table('conditionalstorediscounts')
        self.drop_table('discounts')
        self.drop_table('to_apply_composite')
        self.drop_table('managers')
        self.drop_table('managerpermissions')
        self.drop_table('owners')
        self.drop_table('Policy_in_composite')
        self.drop_table('policies')
        self.drop_table('predicates')
        self.drop_table('products')
        self.drop_table('productspolicies')
        self.drop_table('productsinbaskets')
        self.drop_table('Discount_products')
        self.drop_table('Policy_products')
        self.drop_table('productsinpurcases')
        self.drop_table('purchases')
        self.drop_table('regusers')
        self.drop_table('stores')
        self.drop_table('storepolicies')
        self.drop_table('passwords')
        self.drop_table('notifications')
        self.drop_table('visibleProductDiscounts')

    def drop_table(self, table_name: str):
        if table_name in Base.metadata.tables:
            Base.metadata.drop_all(engine, [Base.metadata.tables[table_name]])

    @classmethod
    def tearDownClass(cls):
        os.remove(
            '/Users/avivlevitzky/PycharmProjects/Workshop/project/tests/domain_layer/stores_managment/tradeSystem.db')


if __name__ == '__main__':
    unittest.main()
