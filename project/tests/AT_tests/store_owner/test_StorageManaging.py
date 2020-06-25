import unittest

import jsons

from project.data_access_layer import Base, engine
from project.tests.AT_tests.test_env.Driver import Driver


class StorageManaging(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.register("owner", "pass")
        self.service.login("owner", "pass")
        self.store_id = self.service.Open_store("my store")

    def test_add_product_to_store_success(self):
        self.assertTrue(self.service.add_product_to_Store(self.store_id, "Banana", 20, "Food", "Fruits", 10))

        # check if was added
        res = self.service.searchProduct("Banana")
        res = jsons.loads(res)
        x=5
        self.assertEqual(self.store_id, res['my store']['store_id'])
        self.assertTrue(res['my store']['search_res'][0]['name'] == "Banana")
        self.assertTrue(res['my store']['search_res'][0]['original_price'] == 20)

    def test_add_product_to_store_sad(self):
        self.service.logout()
        res = self.service.add_product_to_Store(self.store_id, "Banana", 20, "Food", "Fruits", 10)
        x=5
        self.assertTrue(res['error'])

    def test_add_product_to_store_bad(self):
        self.assertTrue(self.service.add_product_to_Store(self.store_id + 40, "Banana", 20, "Food", "Fruits", 10)['error'])

    def test_remove_product_from_store_success(self):
        self.service.add_product_to_Store(self.store_id, "Banana", 20, "Food", "Fruits", 10)

        self.assertTrue(self.service.remove_product_from_store(self.store_id, "Banana"))
        # check if was added
        res = self.service.searchProduct("Banana")
        res = jsons.loads(res)
        self.assertNotIn(self.store_id, res.keys())

    def test_remove_product_from_store_sad(self):
        self.service.logout()
        self.assertEqual('false', self.service.remove_product_from_store(self.store_id, "Banana"))

    def test_remove_product_from_store_bad(self):
        res = jsons.loads(self.service.remove_product_from_store(self.store_id + 40, "Banana"))
        self.assertTrue(res[0]['error'])

    def test_update_product_in_store_success(self):
        self.test_add_product_to_store_success()
        toupdate = {
            "price": 40,
            "categories": ["yellow", "Food"],
            "key_words": ["Fruits"],
            "amount": 40}
        for att in toupdate.keys():
            self.assertTrue(self.service.update_product(self.store_id, "Banana", 100, 20))
        # check if was updated
        res = self.service.searchProduct("Banana")
        res = jsons.loads(res)
        self.assertEqual(self.store_id, res['my store']['store_id'])


    # def test_update_product_in_store_sad(self):
    #     res = jsons.loads(self.service.update_product(self.store_id + 1, "not real product", 100, 700))
    #     self.assertFalse(res['error'])
    #     self.service.logout()
    #     res = jsons.loads(self.service.update_product(self.store_id, "Banana", 100, 10))
    #     self.assertFalse(res['error'])
    #     res = jsons.loads(self.service.update_product(self.store_id, "Banana", 15, -10))
    #     self.assertFalse(res['error'])

    def test_update_product_in_store_bad(self):
        res = jsons.loads(self.service.update_product(self.store_id + 40, "Banana", 100, 10))
        self.assertTrue(res['error'])


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
