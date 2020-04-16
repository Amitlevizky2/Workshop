import unittest
import unittest

from project.tests.AT_tests.test_env.Driver import Driver





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
