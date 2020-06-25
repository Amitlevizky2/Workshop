import unittest
import os
from project.data_access_layer import Base, meta, engine
import jsonpickle
import jsons
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class purchase_History(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        self.service.register("user", "pass")
        self.service.login("user", "pass")
        res = self.service.searchProduct("Banana")
        res_dec = jsons.loads(res)
        # product = res_dec
        first_store_id = res_dec['avishop']["store_id"]
        x=5
        self.service.add_product(first_store_id, "Banana", 2)
        self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)


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
        self.drop_table('passwords')
        self.drop_table('regusers')
        self.drop_table('stores')
        self.drop_table('storepolicies')
        self.drop_table('notifications')
        self.drop_table('visibleProductDiscounts')

    def drop_table(self, table_name: str):
        if table_name in Base.metadata.tables:
            Base.metadata.drop_all(engine, [Base.metadata.tables[table_name]])

    def test_purchase_happy(self):
        result1 = self.service.get_purchase_history()
        result1 = jsons.loads(result1)
        self.assertTrue(result1)

    def test_purchase_bad(self):
        self.service.logout()
        result0 = self.service.get_purchase_history()
        result0 = jsons.loads(result0)
        self.assertTrue(result0)

    def test_purchase_sad(self):
        result1 = self.service.get_purchase_history()
        result1 = jsons.loads(result1)
        self.assertFalse(result1['error'])

if __name__ == '__main__':
    unittest.main()
