import datetime
import unittest

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.NullStore import NullStore
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.users_managment.Basket import Basket
from project.domain_layer.users_managment.Cart import Cart


class StubStore(Store):

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories, key_words: [str],
                    amount) -> bool:
        if user_name != "test_owner" + str(self.store_id):
            return False
        return True

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
        if self.store_id == 4 and search_term == "":
            return []
        return [Product("Banana", 2, ["fruit"], ["fruits"], 2)]

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        return ["hi,i'm a admin view purchase"] if is_admin else ["i'm no admin"]

    def update_product(self, user, product_name, attribute, updated):
        return product_name != "not real product"

    def __init__(self, idx, name, owner):
        Store.__init__(self, idx, name, owner)


class test_StoresManager(unittest.TestCase):
    def setUp(self) -> None:
        self.store_manager = StoresManager()
        for i in range(5):
            self.store_manager.stores[i] = Store(i, "test_store" + str(i), "test_owner" + str(i))
            self.store_manager.stores[i].store_managers["test_owner"] = [Store.add_product, Store.add_visible_product_discount, Store.add_conditional_discount_to_product,
                                                                         Store.update_product]
        self.store_manager.stores_idx = i

        products = self.init_product()
        self.insert_products_to_store(products.values(), self.store_manager.stores.values())
        self.init_discounts()

    def test_update_product(self):
        for store_id in self.store_manager.stores.keys():
            self.assertFalse(
                self.store_manager.update_product(store_id, "test_owner" + str(store_id), "not real product", "price",
                                                  20))
            self.assertTrue(
                self.store_manager.update_product(store_id, "test_owner" + str(store_id), "Apple", "price",
                                                  20))

    def test_search(self):
        self.assertEqual(len(self.store_manager.search("Banana")), 5)
        self.assertEqual(len(self.store_manager.search(key_words=["Fruits"])), 5)

    def test_get_store(self):
        self.assertTrue(isinstance(self.store_manager.get_store(7), NullStore))
        self.test_open_store()
        self.assertTrue(2 == self.store_manager.get_store(2).store_id)

    def test_add_product_to_store(self):
        self.assertFalse(
            self.store_manager.add_product_to_store(7, "not real store", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20))
        self.assertTrue(
            self.store_manager.add_product_to_store(2, "test_owner", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20))
        self.assertTrue(
            self.store_manager.add_product_to_store(2, "test_owner2", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20))

    def test_open_store(self):
        index = self.store_manager.stores_idx
        self.store_manager.open_store("t_ownet", "test")
        self.assertEqual(index + 1, self.store_manager.stores_idx)

    def test_get_sales_history(self):
        self.assertFalse(self.store_manager.get_sales_history(78, "the king", True))
        self.assertFalse(self.store_manager.get_sales_history(0, "some owner", False))
        # self.assertEqual(self.store_manager.get_sales_history(0, "some owner", True)[0], "hi,i'm a admin view purchase")

    def test_add_purchase_store_policy(self):
        is_approved, descr = self.store_manager.add_purchase_store_policy(1, "test_owner1", 3, 8)
        self.assertTrue(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_store_policy(1, "test_owner1", None, None)
        self.assertFalse(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_store_policy(1, "test_owner1", 1, None)
        self.assertTrue(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_store_policy(1, "test_owner2", 1, 2)
        self.assertFalse(is_approved, descr)

    def test_add_purchase_product_policy(self):
        is_approved, descr = self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8)
        self.assertTrue(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_product_policy(1, "test_owner1", None, None)
        self.assertFalse(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_product_policy(1, "test_owner1", 1, None)
        self.assertTrue(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_product_policy(1, "test_owner2", 1, 2)
        self.assertFalse(is_approved, descr)

    def test_add_purchase_composite_policy(self):
        policies_id = self.init_purchases_policies()

        is_approved, descr = self.store_manager.add_purchase_composite_policy(1, "test_owner1", policies_id, "and")
        self.assertTrue(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_composite_policy(1, "test_owner1", [9], "and")
        self.assertFalse(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_composite_policy(2, "test_owner2", policies_id, "xor")
        self.assertTrue(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_composite_policy(3, "test_owner3", policies_id, "or")
        self.assertTrue(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_composite_policy(2, "test_owner2", policies_id, None)
        self.assertFalse(is_approved, descr)
        is_approved, descr = self.store_manager.add_purchase_composite_policy(2, "test_owner5", None, "or")
        self.assertFalse(is_approved, descr)

    def test_add_policy_to_purchase_composite_policy(self):
        policies_id = self.init_purchases_policies()
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8)
        self.store_manager.add_purchase_composite_policy(1, "test_owner1", policies_id, "and")

        is_approved, descr = self.store_manager.add_policy_to_purchase_composite_policy(
            1, "test_owner1", 5, 4)
        self.assertTrue(is_approved, descr)

        is_approved, descr = self.store_manager.add_policy_to_purchase_composite_policy(
            1, "test_owner1", 5, 10)
        self.assertFalse(is_approved, descr)

        is_approved, descr = self.store_manager.add_policy_to_purchase_composite_policy(
            1, "test_owner1", 10, 4)
        self.assertFalse(is_approved, descr)

    def test_add_product_to_purchase_product_policy(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8)

        is_approved, descr = self.store_manager.add_product_to_purchase_product_policy(
            1, 1, "test_owner1", "Apple")

        self.assertTrue(is_approved, descr)

        is_approved, descr = self.store_manager.add_product_to_purchase_product_policy(
            1, 1, "test_owner2", "Orange")

        self.assertFalse(is_approved, descr)

        is_approved, descr = self.store_manager.add_product_to_purchase_product_policy(
            2, 2, "test_owner2", "Orange")

        self.assertFalse(is_approved, descr)

    def test_remove_purchase_policy(self):
        is_approved, descr = self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8)
        self.assertTrue(is_approved, descr)

        is_approved, descr = self.store_manager.remove_purchase_policy(1, "store_owner1", 1)
        self.assertTrue(is_approved, descr)

        is_approved, descr = self.store_manager.remove_purchase_policy(1, "store_owner1", 1)
        self.assertFalse(is_approved, descr)

    def test_remove_product_from_purchase_product_policy(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8)

        is_approved, descr = self.store_manager.add_product_to_purchase_product_policy(
            1, 1, "test_owner1", "Apple")

        self.assertTrue(is_approved, descr)

        is_approved, descr = self.store_manager.remove_product_from_purchase_product_policy(
            1, 1, "test_owner1", "Apple")

        self.assertTrue(is_approved, descr)

    def test_get_discounts(self):
        discounts = self.store_manager.get_discounts(1)
        self.assertEqual(len(discounts), 7)

    def test_get_purchases_policies(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 89)
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)

        self.store_manager.add_purchase_composite_policy(1, "test_owner1", [1, 2], "xor")

        purchases = self.store_manager.get_purchases_policies(1)
        self.assertEqual(2, len(purchases))

    def test_get_purchase_by_id(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8)
        description = self.store_manager.get_purchase_by_id(1, 1)
        is_id = description[0] == 1
        is_type = "Purchase Product Policy" == description[1]
        is_min_amount = '3' == description[2]
        is_max_amount = '8' == description[3]
        self.assertTrue(is_id and is_type and is_min_amount and is_max_amount)

        is_approved, descr = self.store_manager.get_purchase_by_id(6, 1)

        self.assertFalse(is_approved, descr)

        is_approved, descr = self.store_manager.get_purchase_by_id(1, 6)

        self.assertFalse(is_approved, descr)

        is_approved, descr = self.store_manager.get_purchase_by_id(None, 1)

        self.assertFalse(is_approved, descr)

        is_approved, descr = self.store_manager.get_purchase_by_id(6, None)

        self.assertFalse(is_approved, descr)

    def test_check_cart_validity_and(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 89)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 90)

        self.store_manager.add_purchase_composite_policy(2, "test_owner2", [1,2], "and")

        cart = self.init_cart()
        is_approved, descr = self.store_manager.check_cart_validity(cart)
        self.assertFalse(is_approved, descr)

    def test_check_cart_validity_or(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 89)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 90)

        self.store_manager.add_purchase_composite_policy(2, "test_owner2", [1,2], "or")

        cart = self.init_cart()
        is_approved, descr = self.store_manager.check_cart_validity(cart)
        self.assertTrue(is_approved, descr)

    def test_check_cart_validity_xor(self):
        self.store_manager.add_purchase_store_policy(1, "test_owner1", None, 90)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 89)
        self.store_manager.add_purchase_store_policy(2, "test_owner2", None, 90)

        self.store_manager.add_purchase_composite_policy(2, "test_owner2", [1,2], "xor")

        cart = self.init_cart()
        is_approved, descr = self.store_manager.check_cart_validity(cart)
        self.assertTrue(is_approved, descr)

    def test_get_cart_description(self):
        cart = self.init_cart()
        price, description = self.store_manager.get_cart_description(cart)
        x=5

    # def test_get_updated_basket(self):
    #     self.fail()

    def test_get_total_basket_tup_price(self):
        cart = self.init_cart()
        updated = self.store_manager.get_updated_basket(cart.baskets[1])
        price = self.store_manager.get_total_basket_price(updated)
        x = 5

    def test_stores_details(self):
        self.store_manager.add_purchase_product_policy(1, "test_owner1", 3, 8)
        stores_description = self.store_manager.get_stores_description()
        x=5

    def test_buy(self):
        cart = self.init_cart()
        is_apply = self.store_manager.buy(cart)
        x=5

    def test_get_store_jsn_description(self):
        store_json = self.store_manager.get_jsn_description(1)
        x=5



    # def test_get_basket_description(self):
    #     self.fail()

    def init_product(self):
        return {"Apple": Product("Apple", 20, ["Food"], ["Fruits"], 30),
                                         "Banana": Product("Banana", 20, ["Food"], ["Fruits"], 10),
                                         "Orange": Product("Orange", 20, ["Food"], ["Fruits"], 10),
                                         "Tomato": Product("Tomato", 20, ["Food"], ["Vegetables"], 10),
                                         "Cucumber": Product("Cucumber", 20, ["Food"], ["Vegetables"], 10),
                                         "Carrot": Product("Carrot", 20, ["Food"], ["Vegetables"], 10),
                                         "Iphone": Product("Iphone", 20, ["Electronics"], ["Computers"], 10),
                                         "Hard Disk": Product("Hard Disk", 20, ["Electronics"], ["Computers"], 10),
                                         "Keyboard": Product("Keyboard", 20, ["Electronics"], ["Computers"], 10)}

    def init_discounts(self):
        for store in self.store_manager.stores.values():
            str_id = str(store.store_id)
            self.store_manager.add_visible_product_discount(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 30)
            self.store_manager.add_visible_product_discount(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5)
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 2, 2)
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 7, 1)
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 6, 3)
            self.store_manager.add_conditional_discount_to_product(
                store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 100, 3, 1)

            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 1, "Apple")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 4, "Apple")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 4, "Carrot")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 4, "Keyboard")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 5, "Apple")
            self.store_manager.add_product_to_discount(store.store_id, "test_owner" + str_id, 6, "Tomato")


            # self.tup_disc_prod_name_list = []
            # self.tup_disc_prod_name_list.append((self.discount3, ["Apple", "Carrot", "Keyboard"]))
            # self.tup_disc_prod_name_list.append((self.discount4, ["Apple", "Orange"]))
            # self.tup_disc_prod_name_list.append((self.discount5, ["Tomato"]))

            # self.discount6 = CompositeDiscount(store.store_id, "test store", datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
            #                                    LogicOperator.AND,
            #                                    self.tup_disc_prod_name_list, [self.discount, self.discount1])
            # self.discount7 = CompositeDiscount(store.store_id, "test store", datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
            #                                    LogicOperator.OR,
            #                                    self.tup_disc_prod_name_list, [self.discount, self.discount2])
            # self.discount8 = CompositeDiscount(store.store_id, "test store", datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
            #                                    LogicOperator.XOR,
            #                                    self.tup_disc_prod_name_list, [self.discount, self.discount5])

            self.store_manager.add_composite_discount(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17),
                                                      "and", {4: ["Apple", "Carrot", "Keyboard"],
                                                                          5: ["Apple", "Orange"],
                                                                          6: ["Tomato"]}, [1])

    def insert_products_to_store(self, products, stores):
        for store in stores:
            for product in products:
                store.add_product("test_owner", product.name, product.original_price, product.categories,
                                  product.key_words, product.amount)

    def init_cart(self):
        basket = Basket(1)
        basket.products["Apple"] = (self.store_manager.get_store(1).inventory.products["Apple"], 10)
        basket.products["Keyboard"] = (self.store_manager.get_store(1).inventory.products["Keyboard"], 5)
        basket.products["Carrot"] = (self.store_manager.get_store(1).inventory.products["Carrot"], 1)

        basket1 = Basket(2)
        basket1.products["Apple"] = (self.store_manager.get_store(2).inventory.products["Apple"], 10)
        basket1.products["Keyboard"] = (self.store_manager.get_store(2).inventory.products["Keyboard"], 10)
        basket1.products["Carrot"] = (self.store_manager.get_store(2).inventory.products["Carrot"], 10)
        basket1.products["Banana"] = (self.store_manager.get_store(2).inventory.products["Banana"], 10)
        basket1.products["Orange"] = (self.store_manager.get_store(2).inventory.products["Orange"], 10)
        basket1.products["Cucumber"] = (self.store_manager.get_store(2).inventory.products["Cucumber"], 10)
        basket1.products["Iphone"] = (self.store_manager.get_store(2).inventory.products["Iphone"], 10)
        basket1.products["Hard Disk"] = (self.store_manager.get_store(2).inventory.products["Hard Disk"], 10)
        basket1.products["Tomato"] = (self.store_manager.get_store(2).inventory.products["Tomato"], 10)
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
