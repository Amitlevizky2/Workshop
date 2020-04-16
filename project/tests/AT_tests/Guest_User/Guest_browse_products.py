import unittest
import unittest

from project.tests.AT_tests.test_env.Driver import Driver


service = Driver.make_bridge()
storename = "abc"
storeID = 123
product1 = Product("apple watch", 1223, 45, "watches")
product2 = Product("IPhone", 5555, 1000000, "smartphone")
product3 = Product("xiaomi", 4444, 5, "smartphone")
inventory = []
store1 = Store(storename, storeID, inventory.append(product1))


class MyTestCase(unittest.TestCase):



    def test_view_products_happy(self):
        result1 = service.searchProduct(product1.ID,)
        self.assertEquals(self.product1.category, "watches")


    def test_view_products_sad(self):
        self.assertin(self.product2, self.store1.inventory)

    def test_view_products_bad(self):
        self.assertin(None, self.store1.inventory)




if __name__ == '__main__':
    unittest.main()
