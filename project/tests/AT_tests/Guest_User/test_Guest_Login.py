import unittest
from project.tests.AT_tests.test_env.Driver import Driver



class Login(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()
        self.service.register("username","password")
    def test_happy_registration(self):
        res1 = self.service.login("username", "password")
        self.assertTrue(res1)

    def test_sad_registration(self):
        res1 = self.service.login("userNotName", "password")
        self.assertFalse(res1)

    def test_bad_registration(self):
        result1 = self.service.login("", "password")
        self.assertIsNotNone(result1)


if __name__ == '__main__':
    unittest.main()
