from datetime import timedelta, datetime
from unittest import TestCase

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.ProductDiscount import VisibleProductDiscount
from project.domain_layer.users_managment.Basket import Basket
from project.domain_layer.users_managment.Cart import Cart


class TestCart(TestCase):
    def setUp(self) -> None:
        # baskets = {store_id, basket}
        self.cart = Cart()
        date_str = '04-10-2020'
        dt = timedelta(days=100000)
        date_object = datetime.strptime(date_str, '%m-%d-%Y')
        self.product_orange = Product("orange", 2, "food", None, 100)
        self.product_orange.discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_apple = Product("apple", 2, "food", None, 100)
        self.product_apple.discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_petunia = Product("petunia", 5, "food", None, 100)
        self.product_petunia.discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_begonia = Product("begonia", 15, "food", None, 100)
        self.product_begonia.discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))

    def test_add_basket(self):
        # reset baskets & add new basket
        self.cart.baskets.clear()
        self.cart.add_basket(1234)

        self.assertTrue(1234 in self.cart.baskets.keys())

    def test_remove_basket(self):
        self.cart.baskets.clear()

        basket1 = Basket(1234)
        basket2 = Basket(5678)
        self.cart.baskets[1234] = basket1
        self.cart.baskets[5678] = basket2

        self.cart.remove_basket(1234)

        self.assertTrue(1234 not in self.cart.baskets.keys())
        self.assertTrue(5678 in self.cart.baskets.keys())

    def test_get_basket(self):
        self.cart.baskets.clear()
        basket1 = Basket(1234)
        self.cart.baskets[1234] = basket1
        basket2 = self.cart.get_basket(2222)
        basket1_tag = self.cart.get_basket(1234)

        self.assertIsNone(basket2)
        self.assertEqual(basket1, basket1_tag)

    def test_get_total(self):
        self.cart.baskets.clear()
        # total price = 10
        basket1 = Basket(1234)
        basket1.products["orange"] = (self.product_orange, 3)
        basket1.products["apple"] = (self.product_apple, 2)

        # total price = 125
        basket2 = Basket(5678)
        basket2.products["petunia"] = (self.product_petunia, 10)
        basket2.products["begonia"] = (self.product_begonia, 5)

        self.cart.baskets[1234] = basket1
        self.cart.baskets[5678] = basket2

        total_price = self.cart.get_total()
        self.assertEqual(total_price, 67.5)

    def test_view(self):
        pass

    def test_remove_product(self):
        self.cart.baskets.clear()

        basket1 = Basket(1234)
        basket1.products["orange"] = (self.product_orange, 3)
        basket1.products["apple"] = (self.product_apple, 2)

        basket2 = Basket(5678)
        basket2.products["petunia"] = (self.product_petunia, 10)

        self.cart.baskets[1234] = basket1
        self.cart.baskets[5678] = basket2

        self.cart.remove_product(1234, self.product_orange, 3)
        self.cart.remove_product(1234, self.product_apple, 2)
        self.cart.remove_product(5678, self.product_petunia, 5)

        self.assertTrue(1234 not in self.cart.baskets.keys())
        self.assertEqual(basket2.products["petunia"][1], 5)
        self.assertFalse(self.cart.remove_product(5678, self.product_begonia, 5))

    def test_add_product(self):
        pass
