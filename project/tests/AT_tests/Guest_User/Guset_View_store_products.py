import unittest
from Store import Store
from Driver import Driver
from Product import Product

service = Driver.make_bridge()
product1 = Product("apple watch", 1223, 45, "watches")
product2 = Product("IPhone", 5555, 1000000, "smartphone")
product3 = Product("xiaomi", 4444, 5, "smartphone")
inventory = []
store1 = Store("apple", 123, inventory)


class MyTestCase(unittest.TestCase):

    def test_view_products_happy(self):
        result1 = self.service.add_product_to_Store(self.store1.ID, product1.ID)
        self.store1.addProduct(self.product2)
        self.assertin(result1, self.store1.inventory)
        self.assertNotIn(self.product3, self.store1.inventory)

    def test_view_products_sad(self):
        self.assertin(self.product2, self.store1.inventory)

    def test_view_products_bad(self):
        self.assertin(None, self.store1.inventory)


if __name__ == '__main__':
    unittest.main()
