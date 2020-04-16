import unittest

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
        self.assertIn(self.store_id, res.keys())
        self.assertTrue(res.get(self.store_id)[0].name == "Banana")
        self.assertTrue(res.get(self.store_id)[0].price == 20)

    def test_add_product_to_store_sad(self):
        self.service.logout()
        self.assertFalse(self.service.add_product_to_Store(self.store_id, "Banana", 20, "Food", "Fruits", 10))

    def test_add_product_to_store_bad(self):
        self.assertFalse(self.service.add_product_to_Store(self.store_id + 40, "Banana", 20, "Food", "Fruits", 10))

    def test_remove_product_from_store_success(self):
        self.test_add_product_to_store_success()

        self.assertTrue(self.service.remove_product_from_store(self.store_id, "Banana"))
        # check if was added
        res = self.service.searchProduct("Banana")
        self.assertNotIn(self.store_id, res.keys())

    def test_remove_product_from_store_sad(self):
        self.service.logout()
        self.assertFalse(self.service.remove_product_from_store(self.store_id, "Banana"))

    def test_remove_product_from_store_bad(self):
        self.assertFalse(self.service.remove_product_from_store(self.store_id + 40, "Banana"))

    def test_update_product_in_store_success(self):
        self.test_add_product_to_store_success()
        toupdate = {
            "price": 40,
            "categories": ["yellow", "Food"],
            "key_words": ["Fruits"],
            "amount": 40}
        for att in toupdate.keys():
            self.assertTrue(self.service.update_product(self.store_id, "Banana", att, toupdate.get(att)))
        # check if was updated
        res = self.service.searchProduct("Banana")
        self.assertIn(self.store_id, res.keys())
        self.assertTrue(res.get(self.store_id)[0].name == "Banana")
        self.assertTrue(res.get(self.store_id)[0].price == 40)
        self.assertTrue(res.get(self.store_id)[0].categories == ["yellow", "Food"])
        self.assertTrue(res.get(self.store_id)[0].amount == 40)

    def test_update_product_in_store_sad(self):
        self.assertFalse(self.service.update_product(self.store_id, "not real product", "price", 700))
        self.service.logout()
        self.assertFalse(self.service.update_product(self.store_id, "Banana", "price", 10))

        self.assertFalse(self.service.update_product(self.store_id, "Banana", "amount", -10))
    def test_update_product_in_store_bad(self):
        self.assertFalse(self.service.update_product(self.store_id + 40, "Banana", "price", 10))




if __name__ == '__main__':
    unittest.main()
