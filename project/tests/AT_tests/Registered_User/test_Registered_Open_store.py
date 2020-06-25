
import unittest

from project.data_access_layer import Base, engine
from project.tests.AT_tests.test_env.Driver import Driver






class test_Open_store(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        self.service.register("username", "password")
        self.service.login("username", "password")

    def test_open_happy(self):
        result1 = self.service.Open_store("apple")
        managed_stores = self.service.get_managed_stores()
        self.assertIn(result1, managed_stores)

    def test_open_bad(self):
        self.service.logout()
        resutlt1 = self.service.Open_store("Failed")
        self.assertEqual(resutlt1, -1)


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
