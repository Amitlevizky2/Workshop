from datetime import timedelta, datetime
from unittest import TestCase

from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import VisibleProductDiscount
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.users_managment.Basket import Basket


class TestBasket(TestCase):
    def setUp(self) -> None:
        # 1234 for store id
        self.basket = Basket(1234)
        date_str = '04-10-2020'
        dt = timedelta(days=100000)
        date_object = datetime.strptime(date_str, '%m-%d-%Y')
        self.product_orange = Product("orange", 2, "food", None, 100)
        self.product_orange.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_apple = Product("apple", 2, "food", None, 100)
        self.product_apple.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_petunia = Product("petunia", 5, "food", None, 100)
        self.product_petunia.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.product_begonia = Product("begonia", 15, "food", None, 100)
        self.product_begonia.visible_discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))

    def test_get_total(self):
        self.basket.products.clear()
        self.basket.products["orange"] = (self.product_orange, 3)
        total = self.basket.get_total()
        self.assertEqual(total, 3)

    def test_add_product(self):
        # reset products in basket
        self.basket.products.clear()
        self.basket.products["orange"] = (self.product_orange, 3)
        # products test dict contains 5 oranges and 2 apples
        test_products = {}
        pass
        test_products["orange"] = (self.product_orange, 5)
        test_products["apple"] = (self.product_apple, 2)
        # adding 2 oranges and 2 apples to basket
        self.basket.add_product(self.product_orange, 2)
        self.basket.add_product(self.product_apple, 2)
        # test equality of dicts
        self.assertDictEqual(test_products, self.basket.products)

    def test_remove_product(self):
        # reset products in basket
        self.basket.products.clear()
        self.basket.products["orange"] = (self.product_orange, 3)
        # remove all products from basket
        self.basket.remove_product(self.product_orange, 3)
        self.assertDictEqual(self.basket.products, {})


