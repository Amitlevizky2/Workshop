import unittest

import jsons

from project.data_access_layer import Base, engine
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP



class View_store_Products(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)
        self.service.register("user", "pass")
        self.service.login("user","pass")
        self.store_Id = self.service.Open_store("store")
        self.service.add_product_to_Store(self.store_Id,"grape",50,"fruits","little",50)
    def test_view_products_happy(self):
        res = self.service.searchProduct("grape")
        res=jsons.loads(res)
        self.assertEqual(res['store']['search_res'][0]['name'], "grape")



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
