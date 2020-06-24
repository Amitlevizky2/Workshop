import unittest
from project.tests.AT_tests.test_env.Driver import Driver
import os


class Register(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.service = Driver.make_bridge()


    @classmethod
    def tearDownClass(cls):
        os.remove("C:\\Users\\Owner\\Desktop\\Sadna_project\\Workshop\\daldal.db")

    def test_happy_registration(self):
        res1 = self.service.register("username", "password")
        self.assertTrue(res1[0])


    def test_sad_registration(self):

        res1 = self.service.register("username", "password")
        self.assertTrue(res1[0])
        res2 = self.service.register("username", "password")

        self.assertFalse(res2[0])




if __name__ == '__main__':
    unittest.main()
