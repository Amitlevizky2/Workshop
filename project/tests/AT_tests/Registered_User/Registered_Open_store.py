
import unittest

from Driver import Driver


service = Driver.make_bridge()



class test_Open_store(unittest.TestCase):
    def setUp(self):
        service.register("username", "password")
        service.login("username", "password")

    def test_open_happy(self):
        result1 = service.Open_store("apple")
        self.assertIn(result1, service.get_managed_stores())

    def test_open_bad(self):
        service.logout()
        resutlt1 = service.Open_store("Failed")
        self.assertEqual(resutlt1, -1)




if __name__ == '__main__':
    unittest.main()
