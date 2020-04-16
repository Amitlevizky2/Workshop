from unittest import TestCase

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.User import User


class TestUser(TestCase):
    def setUp(self) -> None:
        self.user = User("Shem")
        self.product_orange = Product("orange", 2, "food", None, 100)
        self.purchase = Purchase([self.product_orange], "Shem", 1234, 1)

    def test_view_cart(self):
        pass

    # tested in test_Cart
    def test_remove_product(self):
        pass

    # tested in test_Cart and in test_Basket
    def test_add_product(self):
        pass

    def test_get_cart(self):
        pass

    def test_remove_cart(self):
        pass

    def test_add_purchase(self):
        self.user.purchase_history.clear()
        self.user.add_purchase(self.purchase)
        self.assertEqual(self.user.purchase_history.pop(0), self.purchase)
