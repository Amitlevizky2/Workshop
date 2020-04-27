
import unittest

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




if __name__ == '__main__':
    unittest.main()
