import datetime
import unittest

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.NullStore import NullStore
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.Basket import Basket


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
            self.store_manager.stores[i].store_managers["test_owner"] = [Store.add_product, Store.add_visible_discount_to_product, Store.add_conditional_discount_to_product]
        self.store_manager.stores_idx = i

        products = self.init_product()
        self.insert_products_to_store(products.values(), self.store_manager.stores.values())
        self.init_discounts()
        x=5

    def test_update_product(self):
        for store_id in self.store_manager.stores.keys():
            self.assertFalse(
                self.store_manager.update_product(store_id, "test_owner" + str(store_id), "not real product", "price",
                                                  20))
            self.assertTrue(
                self.store_manager.update_product(store_id, "test_owner" + str(store_id), "real product", "price",
                                                  20))

    def test_search(self):
        self.assertEqual(len(self.store_manager.search("Banana")), 5)
        self.assertEqual(len(self.store_manager.search(categories=["fruit"])), 4)

    def test_get_store(self):
        self.assertTrue(isinstance(self.store_manager.get_store(7), NullStore))
        self.test_open_store()
        self.assertTrue(2 == self.store_manager.get_store(2).store_id)

    def test_add_product_to_store(self):
        self.assertFalse(
            self.store_manager.add_product_to_store(7, "not real store", "what a product", 1222, ["imaginary products"],
                                                    ["no"], 20))
        self.assertFalse(
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
        self.assertEqual(self.store_manager.get_sales_history(0, "some owner", False)[0], "i'm no admin")
        self.assertEqual(self.store_manager.get_sales_history(0, "some owner", True)[0], "hi,i'm a admin view purchase")

    def test_add_purchase_store_policy(self):
        self.fail()

    def test_add_purchase_product_policy(self):
        self.fail()

    def test_add_purchase_composite_policy(self):
        self.fail()

    def test_add_policy_to_purchase_composite_policy(self):
        self.fail()

    def test_add_product_to_purchase_product_policy(self):
        self.fail()

    def test_remove_purchase_policy(self):
        self.fail()

    def test_remove_product_from_purchase_product_policy(self):
        self.fail()

    def test_get_discounts(self):
        discounts = self.store_manager.get_discounts(1)
        self.assertDictEqual(self.store_manager.stores[1].discounts, discounts)

    def test_get_discount_details(self):
        discount = self.store_manager.get_discount_details(1, 7)
        self.assertEqual("Composite Discount", discount.discount_type)

    def test_get_purchases_policies(self):
        self.fail()

    def test_get_purchase_by_id(self):
        self.fail()

    def test_check_basket_validity(self):
        self.fail()

    def test_get_cart_description(self):
        cart = self.init_cart()
        price, description = self.store_manager.get_cart_description(cart)
        x=5

    def test_get_updated_basket(self):
        self.fail()

    def test_get_total_basket_price(self):
        self.fail()

    def test_get_basket_description(self):
        self.fail()

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
            self.store_manager.add_visible_discount_to_product(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5)
            self.store_manager.add_visible_discount_to_product(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5)
            self.store_manager.add_conditional_discount_to_product(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 2,
                                                        2)
            self.store_manager.add_conditional_discount_to_product(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 7,
                                                        1)
            self.store_manager.add_conditional_discount_to_product(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 5, 6,
                                                        3)
            self.store_manager.add_conditional_discount_to_product(store.store_id, "test_owner" + str_id, datetime.datetime(2018, 6, 1), datetime.datetime(2020, 5, 17), 100,
                                                        3, 1)

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
                                                      LogicOperator.AND, {4: ["Apple", "Carrot", "Keyboard"],
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


if __name__ == '__main__':
    unittest.main()
