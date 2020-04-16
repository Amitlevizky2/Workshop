import unittest

from project.tests.AT_tests.test_env.Driver import Driver


class open_store(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        self.service.register("username","password")
        self.service.login("username","password")
    def test_open_store_happy(self):
        res1 = self.service.Open_store("apple")
        self.assertEqual(res1, 0)

    def test_open_store_bad(self):
        res1 = self.service.logout("")
        if res1:
            res1 = -1
        res2 = self.service.Open_store("Failed")
        self.assertEqual(res1,res2)




if __name__ == '__main__':
    unittest.main()
