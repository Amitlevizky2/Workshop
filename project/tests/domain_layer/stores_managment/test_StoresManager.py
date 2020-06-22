import datetime
import unittest

import jsons

from project.domain_layer.stores_managment.NullStore import NullStore
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.users_managment.Basket import Basket
from project.domain_layer.users_managment.Cart import Cart
from project.tests.domain_layer.stores_managment.Stubs.StoreStub import StoreStub
import project.data_access_layer
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


class test_StoresManager(unittest.TestCase):
    def setUp(self) -> None:

        path = 'sqlite:////Users/avivlevitzky/PycharmProjects/Workshop/project/test.db'
        Base = declarative_base()
        session = sessionmaker()
        engine = create_engine(path, echo=True)
        session.configure(bind=engine)
        session = Session()




        self.store_manager = StoresManager()
        # self.stores_getters = StoresGetters(self.store_manager)
        for i in range(5):
            self.store_manager.stores[i] = Store(i, "test_store" + str(i), "test_owner" + str(i))
            self.store_manager.stores[i].store_managers["test_owner"] = [Store.add_product, Store.add_visible_product_discount, Store.add_conditional_discount_to_product,
                                                                         Store.update_product]
            self.store_manager.stores_idx = i

        # products = self.init_product()
        # self.insert_products_to_store(products.values(), self.store_manager.stores.values())
        # self.init_discounts()
        self.init_stores()

    def init_stores(self):
        # create stab stores
        store11 = StoreStub(11, "store11", "store_owner11")
        store12 = StoreStub(12, "store12", "store_owner12")
        store13 = StoreStub(13, "store13", "store_owner13")
        store14 = StoreStub(14, "store14", "store_owner14")
        store15 = StoreStub(15, "store15", "store_owner15")

        self.store_manager.stores[11] = store11
        self.store_manager.stores[12] = store12
        self.store_manager.stores[13] = store13
        self.store_manager.stores[14] = store14
        self.store_manager.stores[15] = store15

    def test_appoint_manager_to_store(self):
        res1 = self.store_manager.appoint_manager_to_store(11, 'store_owner11', 'manager')
        res2 = self.store_manager.appoint_manager_to_store(11, 'store_owner', 'manager')
        res3 = self.store_manager.appoint_manager_to_store(11, 'store_owner11', 'manage')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_appoint_owner_to_store(self):
        res1 = self.store_manager.appoint_owner_to_store(11, 'store_owner11', 'owner')
        res2 = self.store_manager.appoint_owner_to_store(11, 'store_owner', 'owner')
        res3 = self.store_manager.appoint_owner_to_store(11, 'store_owner11', 'owne')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_add_permission_to_manager_in_store(self):
        res1 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner11', 'manager', 'add_product')
        res2 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner', 'manager', 'add_product')
        res2 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner11', 'owner', 'add_prod')
        res3 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner11', 'manag', 'add_product')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_remove_permission_from_manager_in_store(self):
        res1 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner11', 'manager', 'add_product')
        res2 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner', 'manager', 'add_product')
        res2 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner11', 'owner', 'add_prod')
        res3 = self.store_manager.add_permission_to_manager_in_store(11, 'store_owner11', 'manag', 'add_product')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_remove_product(self):
        res1 = self.store_manager.remove_product_from_store(11, 'Banana' ,'store_owner11')
        res2 = self.store_manager.remove_product_from_store(11, 'Bana' ,'store_owner11')
        res3 = self.store_manager.remove_product_from_store(11, 'Banana' ,'store_owner')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_remove_manager(self):
        res1 = self.store_manager.remove_manager(11, 'store_owner11', 'manager')
        res2 = self.store_manager.remove_manager(11, 'store_owner', 'manage')
        res3 = self.store_manager.remove_manager(11, 'srr', 'manager')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_remove_owner(self):
        res1 = self.store_manager.remove_owner(11, 'store_owner11', 'to_remove')
        res2 = self.store_manager.remove_owner(11, 'store_owner', 'remoeme')
        res3 = self.store_manager.remove_owner(11, 'srr', 'to_remove')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_get_discount_details(self):
        res1 = self.store_manager.get_discount_details(11, 1)
        res1 = jsons.loads(res1)
        self.assertFalse(res1['error'])
        self.assertIsNotNone(res1['discount'])

    def test_add_visible_product_discount(self):
        res1 = self.store_manager.add_visible_product_discount(11, 'store_owner11',
                                                               datetime.datetime(2018, 6, 1),
                                                               datetime.datetime(2020, 12, 17),
                                                               5, [])
        res1 = jsons.loads(res1)
        self.assertFalse(res1['error'])
        self.assertEqual(1, res1['data']['discount_id'])

    def test_add_conditional_discount_to_product(self):
        res1 = self.store_manager.add_conditional_discount_to_product(11, 'store_owner11',
                                                               datetime.datetime(2018, 6, 1),
                                                               datetime.datetime(2020, 12, 17),
                                                               5, 5, 5, [])
        res1 = jsons.loads(res1)
        self.assertFalse(res1['error'])
        self.assertEqual(1, res1['data']['discount_id'])

    def test_add_product_to_discount(self):
        res1 = self.store_manager.add_product_to_discount(11, 'store_owner11', 1, 'Banana')
        res2 = self.store_manager.add_product_to_discount(11, 'store_owner11', 1, 'Baa')
        res3 = self.store_manager.add_product_to_discount(11, 'store_owne', 1, 'Banana')
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_remove_product_from_discount(self):
        res1 = self.store_manager.remove_product_from_discount(11, 'store_owner11', 1, 'Banana')
        res2 = self.store_manager.remove_product_from_discount(11, 'store_owner11', 1, 'Baa')
        res3 = self.store_manager.remove_product_from_discount(11, 'store_owne', 1, 'Banana')
        res1 = jsons.loads(res1)
        res2 = jsons.loads(res2)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])


    def test_add_composite_discount(self):
        res1 = self.store_manager.add_composite_discount(11,
                                                         "store_owner11",
                                                         datetime.datetime(2018, 6, 1),
                                                         datetime.datetime(2020, 12, 17),
                                                         "and", {1: ['Banana']}, [1])
        res1 = jsons.loads(res1)
        self.assertFalse(res1)

    # def test_add_composite_discount(self):
    #     res1 = self.store_manager.add_composite_discount(11,
    #                                                      "store_owner11",
    #                                                      datetime.datetime(2018, 6, 1),
    #                                                      datetime.datetime(2020, 12, 17),
    #                                                      "and", {1: ['Banana']}, [1])
    #     res1 = jsons.loads(res1)
    #     self.assertFalse(res1['error'])
    #
    # def test_add_composite_discount(self):
    #     res1 = self.store_manager.add_composite_discount(11,
    #                                                      "store_owner11",
    #                                                      datetime.datetime(2018, 6, 1),
    #                                                      datetime.datetime(2020, 12, 17),
    #                                                      "and", {1: ['Banana']}, [1])
    #     res1 = jsons.loads(res1)
    #     self.assertFalse(res1['error'])

    def test_edit_visible_discount_to_product(self):
        self.fail()

    def test_edit_conditional_discount_to_product(self):
        self.fail()

    def test_get_user_permissions(self):
        res1 = self.store_manager.get_user_permissions(11, 'store_owner11')
        res3 = self.store_manager.get_user_permissions(11, 'store_owne')
        res1 = jsons.loads(res1)
        res3 = jsons.loads(res3)
        self.assertFalse(res1['error'])
        self.assertTrue(res3['error'])

    def test_is_valid_amount(self):
        res1 = self.store_manager.is_valid_amount(11, 'Banana', 12)
        res2 = self.store_manager.is_valid_amount(11, 'Banana', 11)
        res3 = self.store_manager.is_valid_amount(11, 'Bana22na', 12)
        self.assertFalse(res1['error'])
        self.assertTrue(res2['error'])
        self.assertTrue(res3['error'])

    def test_update_product(self):
        for store_id in self.store_manager.stores.keys():
            res = self.store_manager.update_product(store_id, "test_owner" + str(store_id), "not real product", "price",
                                                  20)
            res = jsons.loads(res)
            self.assertTrue(res['error'])

            res = self.store_manager.update_product(store_id, "test_owner" + str(store_id), "Apple", "price",
                                                  20)
            res = jsons.loads(res)
            self.assertTrue(res)

    def test_search(self):
        res = self.store_manager.search("Banana")
        res = jsons.loads(res)
        self.assertEqual(len(res.keys()), 5)
        res = self.store_manager.search(key_words=["Fruits"])
        res = jsons.loads(res)
        self.assertEqual(len(res), 5)

    def test_get_store(self):
        self.assertTrue(isinstance(self.store_manager.get_store(7), NullStore))
        self.test_open_store()
        self.assertTrue(2 == self.store_manager.get_store(2).store_id)

    def test_add_product_to_store(self):
        res = self.store_manager.add_product_to_store(7, "not real store", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20)
        res = jsons.loads(res)
        self.assertFalse(res['error'])
        res = self.store_manager.add_product_to_store(2, "test_owner", "what a product", 1222, ["imaginary products"],
                                                ["no"], 20)
        res = jsons.loads(res)
        self.assertTrue(res['error'])
        res = self.store_manager.add_product_to_store(2, "test_owner2", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20)
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def test_open_store(self):
        index = self.store_manager.stores_idx
        self.store_manager.open_store("t_ownet", "test")
        self.assertEqual(index + 1, self.store_manager.stores_idx)

    def test_get_sales_history(self):
        cart = self.init_cart()
        is_apply = self.store_manager.buy(cart)

        sales = self.store_manager.get_sales_history(1, 'test_owner1', True)

        # self.assertFalse(self.store_manager.get_sales_history(78, "the king", True))
        # self.assertFalse(self.store_manager.get_sales_history(0, "some owner", False))
        # self.assertEqual(self.store_manager.get_sales_history(0, "some owner", True)[0], "hi,i'm a admin view purchase")

    def test_add_purchase_store_policy(self):
        res = self.store_manager.add_purchase_store_policy(1, "test_owner1", 3, 8)
        res = jsons.loads(res)
        self.assertFalse(res['error'])
        res = self.store_manager.add_purchase_store_policy(1, "test_owner1", None, None)
        res = jsons.loads(res)
        self.assertFalse(res['ans'])
        res = self.store_manager.add_purchase_store_policy(1, "test_owner1", 1, None)
        res = jsons.loads(res)
        self.assertFalse(res['error'])
        res = self.store_manager.add_purchase_store_policy(1, "test_owner2", 1, 2)
        res = jsons.loads(res)
        self.assertFalse(res['ans'])

    def test_add_purchase_product_policy(self):
        res = self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8, ['Banana'])
        # self.assertTrue(res)
        res = self.store_manager.add_purchase_product_policy(1, "test_owner1", None, None, ['Banana'])
        # self.assertFalse(res)
        res = self.store_manager.add_purchase_product_policy(1, "test_owner1", 1, None, ['Banana'])
        # self.assertTrue(res)
        res = self.store_manager.add_purchase_product_policy(1, "test_owner2", 1, 2, ['Banana'])
        # self.assertFalse(res)

    def test_add_purchase_composite_policy(self):
        policies_id = self.init_purchases_policies()

        res = self.store_manager.add_purchase_composite_policy(1, "test_owner1", policies_id, "and")
        # self.assertTrue(res)
        res = self.store_manager.add_purchase_composite_policy(1, "test_owner1", [9], "and")
        # self.assertFalse(res)
        res = self.store_manager.add_purchase_composite_policy(2, "test_owner2", policies_id, "xor")
        # self.assertTrue(res)
        res = self.store_manager.add_purchase_composite_policy(3, "test_owner3", policies_id, "or")
        # self.assertTrue(res)
        res = self.store_manager.add_purchase_composite_policy(2, "test_owner2", policies_id, None)
        # self.assertFalse(res)
        res = self.store_manager.add_purchase_composite_policy(2, "test_owner5", None, "or")
        # self.assertFalse(res) TODO: add tests

    def test_add_policy_to_purchase_composite_policy(self):
        policies_id = self.init_purchases_policies()
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8, ['Banana'])
        self.store_manager.add_purchase_composite_policy(1, "test_owner1", policies_id, "and")

        res = self.store_manager.add_policy_to_purchase_composite_policy(
            1, "test_owner1", 5, 4)
        # self.assertTrue(res)

        res = self.store_manager.add_policy_to_purchase_composite_policy(
            1, "test_owner1", 5, 10)
        # self.assertFalse(res['error'])

        res = self.store_manager.add_policy_to_purchase_composite_policy(
            1, "test_owner1", 10, 4)
        # self.assertFalse(res)

    def test_add_product_to_purchase_product_policy(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8, ['Banana'])

        res = self.store_manager.add_product_to_purchase_product_policy(
            1, 1, "test_owner1", "Apple")

        # self.assertTrue(res)

        res = self.store_manager.add_product_to_purchase_product_policy(
            1, 1, "test_owner2", "Orange")

        # self.assertFalse(res)

        res = self.store_manager.add_product_to_purchase_product_policy(
            2, 2, "test_owner2", "Orange")

        # self.assertFalse(res) TODO: tests

    def test_remove_purchase_policy(self):
        res = self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8, ['Banana'])
        # self.assertTrue(res)

        res = self.store_manager.remove_purchase_policy(1, "store_owner1", 1)
        # self.assertTrue(res)

        res = self.store_manager.remove_purchase_policy(1, "store_owner1", 1)
        # self.assertFalse(res)

    def test_remove_product_from_purchase_product_policy(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8, ['Banana'])

        res = self.store_manager.add_product_to_purchase_product_policy(
            1, 1, "test_owner1", "Apple")

        self.assertTrue(res)

        res = self.store_manager.remove_product_from_purchase_product_policy(
            1, 1, "test_owner1", "Apple")

        # self.assertTrue(res) TODO: test

    def test_get_discounts(self):
        discounts = self.store_manager.get_discounts(1)
        # self.assertEqual(len(discounts), 7) TODO: tests

    def test_get_purchases_policies(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 89)
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)

        self.store_manager.add_purchase_composite_policy(1, "test_owner1", [1, 2], "xor")

        purchases = jsons.load(self.store_manager.get_purchases_policies(1))
        self.assertTrue(purchases['ans'])
        purchases = purchases['policies']
        self.assertEqual(2, len(purchases))

    def test_get_purchase_by_id(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8, ['Banana'])
        description = self.store_manager.get_purchase_policy_by_id(1, 1)
        description = jsons.loads(description)
        self.assertTrue(description['ans'])
        description = description['desc']
        min = description['min_amount_products']
        max = description['max_amount_products']
        self.assertEqual(min, 3)
        self.assertEqual(max, 8)

    def test_check_cart_validity_and(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 89)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 90)

        self.store_manager.add_purchase_composite_policy(2, "test_owner2", [1, 2], "and")

        cart = self.init_cart()
        res = self.store_manager.check_cart_validity(cart)
        res = jsons.loads(res)
        self.assertTrue(res['error'])

    def test_check_cart_validity_or(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 89)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 90)

        self.store_manager.add_purchase_composite_policy(2, "test_owner2", [1,2], "or")

        cart = self.init_cart()
        res = self.store_manager.check_cart_validity(cart)
        x=5

    def test_check_cart_validity_xor(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 89)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 90)

        self.store_manager.add_purchase_composite_policy(2, "test_owner2", [1,2], "xor")

        cart = self.init_cart()
        res = self.store_manager.check_cart_validity(cart)
        x=5

    def test_get_cart_description(self):
        cart = self.init_cart()
        cart = jsons.loads(self.store_manager.get_cart_description(cart))
        self.assertTrue(cart['ans'])
        self.assertEqual(cart['cart_price'], 2060.0)
        cart = cart['cart_description']
        store = cart['test_store1']
        desc = store['desc']
        product = desc['Apple']
        apple_price = product['price_after_disc']
        self.assertEqual(apple_price, 196.0)

    def test_get_total_basket_tup_price(self):
        cart = self.init_cart()
        updated = self.store_manager.get_updated_basket(cart.baskets[1])
        price = self.store_manager.get_total_basket_price(updated)
        x = 5

    def test_stores_details(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8, ['Banana'])
        stores_description = jsons.loads(self.store_manager.get_stores_description())
        self.assertFalse(stores_description['error'])
        stores_description = stores_description['data']
        self.assertEqual(len(stores_description.keys()), 5)

    def test_buy(self):
        cart = self.init_cart()
        is_apply = self.store_manager.buy(cart)
        x=5

    def test_get_product_from_store(self):
        product = jsons.loads(self.store_manager.get_product_from_store(1, "Apple"))
        self.assertTrue(product['ans'])
        product = product['product']
        self.assertEqual(product['amount'], 30)

    def test_get_inventory_description(self):
        inventory = jsons.loads(self.store_manager.get_inventory_description(1))
        products = inventory['inventory']['products']
        self.assertTrue(len(products.keys()) == 9)

    def test_get_store_managers(self):
        managers = jsons.loads(self.store_manager.get_store_managers(1))
        self.assertFalse(managers['error'])
        managers = managers['data']
        self.assertTrue(len(managers) == 1)
        # self.assertTrue(len(managers['test_owner']) == 4)

    def test_get_store_owners(self):
        owners = self.store_manager.get_store_owners(1)
        owners = jsons.loads(owners)
        self.assertFalse(owners['error'])
        owners = owners['data']
        self.assertIn('test_owner1', owners)


    # def test_get_basket_description(self):
    #     self.fail()

    def init_product(self):
        return {"Apple": Product("Apple", 20, ["Food"], ["Fruits"], 30, 0),
                                         "Banana": Product("Banana", 20, ["Food"], ["Fruits"], 10, 0),
                                         "Orange": Product("Orange", 20, ["Food"], ["Fruits"], 10, 0),
                                         "Tomato": Product("Tomato", 20, ["Food"], ["Vegetables"], 10, 0),
                                         "Cucumber": Product("Cucumber", 20, ["Food"], ["Vegetables"], 10, 0),
                                         "Carrot": Product("Carrot", 20, ["Food"], ["Vegetables"], 10, 0),
                                         "Iphone": Product("Iphone", 20, ["Electronics"], ["Computers"], 10, 0),
                                         "Hard Disk": Product("Hard Disk", 20, ["Electronics"], ["Computers"], 10, 0),
                                         "Keyboard": Product("Keyboard", 20, ["Electronics"], ["Computers"], 10, 0)}

    def init_discounts(self):
        for store in self.store_manager.stores.values():
            str_id = str(store.store_id)
            self.store_manager.add_visible_product_discount(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 30, [])
            self.store_manager.add_visible_product_discount(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 5, [])
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 5, 2, 2, [])
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 5, 7, 1, [])
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 5, 6, 3, [])
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 100, 3, 1, [])

            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 1, "Apple")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 1, "Banana")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 2, "Banana")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 4, "Apple")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 4, "Carrot")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 4, "Keyboard")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 5, "Apple")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 6, "Tomato")
            self.store_manager.add_composite_discount(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17),
                                                      "and", {4: ["Apple", "Carrot", "Keyboard"],
                                                                          5: ["Apple", "Orange"],
                                                                          6: ["Tomato"]}, [1])

    def insert_products_to_store(self, products, stores):
        for store in stores:
            for product in products:
                store.add_product("test_owner" + str(store.store_id), product.name, product.original_price, product.categories,
                                  product.key_words, product.amount)

    def init_cart(self):
        basket = Basket(1)
        basket.products["Apple"] = 10
        basket.products["Keyboard"] = 5
        basket.products["Carrot"] = 1

        basket1 = Basket(2)
        basket1.products["Apple"] = 10
        basket1.products["Keyboard"] = 10
        basket1.products["Carrot"] = 10
        basket1.products["Banana"] = 10
        basket1.products["Orange"] = 10
        basket1.products["Cucumber"] = 10
        basket1.products["Iphone"] = 10
        basket1.products["Hard Disk"] = 10
        basket1.products["Tomato"] = 10
        cart = Cart()
        cart.baskets[1] = basket
        cart.baskets[2] = basket1
        return cart

    def init_purchases_policies(self):
        for store in self.store_manager.stores.values():
            str_id = str(store.store_id)
            self.store_manager.add_purchase_store_policy(store.store_id, "test_owner" + str_id, 3, 8)
            self.store_manager.add_purchase_store_policy(store.store_id, "test_owner" + str_id, 1, 10)
            self.store_manager.add_purchase_store_policy(store.store_id, "test_owner" + str_id, 5, 6)
            x=5
        return [p for p in self.store_manager.get_store(1).purchase_policies.keys()]


if __name__ == '__main__':
    unittest.main()
