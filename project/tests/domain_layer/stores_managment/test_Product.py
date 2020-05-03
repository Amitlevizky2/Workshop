import unittest
from datetime import datetime, timedelta

from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.ProductDiscount import ProductDiscount, VisibleProductDiscount


class test_Product(unittest.TestCase):
    def test_get_price(self):
        date_str = '04-10-2020'
        dt = timedelta(days=10)
        date_object = datetime.strptime(date_str, '%m-%d-%Y')
        self.product = Product("apple", 2, "food", None, 1)
        self.product.discount.append(VisibleProductDiscount(date_object, date_object + dt, 50))
        self.assertEqual(1, self.product.get_price())
