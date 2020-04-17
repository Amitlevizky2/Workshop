import unittest
from project.tests.AT_tests.test_env.Driver import Driver

from project.tests.AT_tests import ATsetUP
class purchase_History(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)

        self.service.register("user","pass")
        self.service.login("user", "pass")
        res = self.service.searchProduct("Banana")
        first_store_id = list(res)[0]
        self.service.add_product(first_store_id,res.get(first_store_id)[0], 2)
        self.service.buy()
    def test_purchase_happy(self):
        result = self.service.get_purchase_history()
        self.assertEqual(list(result[0].products)[0], "Banana")

    def test_purchase_bad(self):
        self.service.logout()
        result = self.service.get_purchase_history()
        self.assertTrue(len(result)==0)


    def test_purchase_sad(self):
        res1 = self.service.get_purchase_history()
        self.assertNotEqual(list(res1[0].products)[0], "marshmelo")



if __name__ == '__main__':
    unittest.main()
