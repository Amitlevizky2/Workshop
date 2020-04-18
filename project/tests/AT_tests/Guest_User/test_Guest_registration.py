import unittest
from project.tests.AT_tests.test_env.Driver import Driver


class Register(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()


    def test_happy_registration(self):
        res1 = self.service.register("username", "password")
        self.assertTrue(res1)

    def test_sad_registration(self):
        res1 = self.service.register("username", "password")
        res2 = self.service.register("username", "password")
        self.assertTrue(res1)
        self.assertFalse(res2)




if __name__ == '__main__':
    unittest.main()
