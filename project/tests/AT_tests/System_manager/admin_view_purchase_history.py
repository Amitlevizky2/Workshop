import unittest
from project.tests.AT_tests.test_env.Driver import Driver


class admin_view_purchase_history(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()
        self.service.register("admin","admin")
        self.service.login("admin","admin")
        self.service.register("user","pass")
        self.service.login("user","pass")
        res = self.service.searchProduct("Banana")
        first_store_id = list(res)[0]
        self.service.add_product(first_store_id, res.get(first_store_id), 2)
        self.service.buy()

    def test_admin_view_happy(self):
        if self.service.admin:
            result = self.service.get_purchase_history()
            self.assertEqual(result.products[0].name, "Banana")


if __name__ == '__main__':
    unittest.main()
