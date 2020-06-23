import unittest
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP
import jsons


class purchase_products_by_purchase_types(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        res = self.service.searchProduct("Banana")
        res = jsons.loads(res)

        first_store_id = list(res)[0]
        self.service.add_product(res.get(first_store_id)['store_id'], res.get(first_store_id)['search_res'][0]['name'],
                                 2)
        self.service.buy(654651, 1, 2025, "ani", 545, 31684321, "my house", "atlantis", "ocean", 987654)

    def test_buy_by_type_purchase_happy(self):
        result = self.service.get_purchase_history()

        self.assertEqual(list(jsons.loads(result[1][0]['products']).keys())[0], "Banana")

    def test_buy_by_type_purchase_sad(self):
        res = self.service.searchProduct("Apple")
        res = jsons.loads(res)
        first_store_id = list(res)[0]
        self.service.add_product(res.get(first_store_id)['store_id'], res.get(first_store_id)['search_res'][0]['name'],
                                 2)
        self.service.buy(654651, 1, 2025, "ani", 545, 31684321, "my house", "atlantis", "ocean", 987654)
        result = self.service.get_purchase_history()
        self.assertNotIn("apple", list(jsons.loads(result[1][0]['products']).keys()))

    def test_buy_by_type_purchase_bad(self):
        res = self.service.searchProduct("Banana")
        res = jsons.loads(res)

        first_store_id = list(res)[0]
        self.service.add_product(res.get(first_store_id)['store_id'], res.get(first_store_id)['search_res'][0]['name'],
                                 2)
        self.service.buy(654651, 1, 2025, "ani", 545, 31684321, "my house", "atlantis", "ocean", 987654)
        result = self.service.get_purchase_history()
        self.service.logout()
        self.assertIn("Banana", list(jsons.loads(result[1][0]['products']).keys()))


if __name__ == '__main__':
    unittest.main()
