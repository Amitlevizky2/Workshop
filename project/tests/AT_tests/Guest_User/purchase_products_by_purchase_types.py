import unittest

from project.data_access_layer import Base, engine
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


    def tearDown(self) -> None:
        self.drop_table('stores')
        self.drop_table('baskets')
        self.drop_table('CompositeDiscounts')
        self.drop_table('CompositePolicies')
        self.drop_table('conditionalproductdiscounts')
        self.drop_table('conditionalstorediscounts')
        self.drop_table('discounts')
        self.drop_table('to_apply_composite')
        self.drop_table('managers')
        self.drop_table('managerpermissions')
        self.drop_table('owners')
        self.drop_table('Policy_in_composite')
        self.drop_table('policies')
        self.drop_table('predicates')
        self.drop_table('products')
        self.drop_table('productspolicies')
        self.drop_table('productsinbaskets')
        self.drop_table('Discount_products')
        self.drop_table('Policy_products')
        self.drop_table('productsinpurcases')
        self.drop_table('purchases')
        self.drop_table('regusers')
        self.drop_table('stores')
        self.drop_table('storepolicies')
        self.drop_table('passwords')
        self.drop_table('notifications')
        self.drop_table('visibleProductDiscounts')
        # self.drop_table('stores')

    def drop_table(self, table_name: str):
        if table_name in Base.metadata.tables:
            Base.metadata.drop_all(engine, [Base.metadata.tables[table_name]])

if __name__ == '__main__':
    unittest.main()
