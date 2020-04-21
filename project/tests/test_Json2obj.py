import unittest
from datetime import datetime, timedelta

from project.domain_layer.stores_managment.Product import Product, Discount
from project.utils import Json2obj

class test_Json2obj(unittest.TestCase):
    def test_product_to_json(self):
        date_str = '04-10-2020'
        dt = timedelta(days=10)
        date_object = datetime.strptime(date_str, '%m-%d-%Y')
        p=Product("Apple", 20, "Food", "Fruits", 10)
        p.discount.append(Discount(date_object, date_object + dt, 50))
        print(Json2obj.product_to_json(p))
    def test_json_to_product(self):
        date_str = '04-10-2020'
        dt = timedelta(days=10)
        date_object = datetime.strptime(date_str, '%m-%d-%Y')
        p = Product("Apple", 20, "Food", "Fruits", 10)
        p.discount.append(Discount(date_object, date_object + dt, 50))
        json_p =Json2obj.json_to_product(Json2obj.product_to_json(p))
        print(json_p)
