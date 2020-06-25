import unittest

import jsons

from project.data_access_layer import Base, engine
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class ViewStoreHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.login("avi", "123")
        products = self.service.searchProduct("Apple")
        self.service.add_product(self.store_id, "Apple", 3)
        self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)

    def test_view_store_history_success(self):
        history = jsons.load(self.service.view_store_history(self.store_id))
        x=3
        self.assertIsNotNone(history)
        x=5
        self.assertIn("Apple", history['data'][0]['products'].keys())

    def test_view_store_history_sad(self):
        self.service.logout()
        history = jsons.loads(self.service.view_store_history(self.store_id))
        self.assertTrue(history['error'])



    def test_view_store_history_bad(self):
        history = self.service.view_store_history(self.store_id+40)
        history = jsons.loads(history)
        self.assertTrue(history['error'])

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
