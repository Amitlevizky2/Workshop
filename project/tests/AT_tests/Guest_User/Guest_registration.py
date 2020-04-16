import unittest
from project.tests.AT_tests.test_env.Driver import Driver





class Register(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()

        res2 =self.service.register("username","password")
    def test_happy_registration(self):
        res1 = self.service.register("username", "password")
        self.assertTrue(res1)

    def test_sad_registration(self):
        res1 = self.service.register("username", "password")
        res2 = self.service.register("username","password")
        self.assertEqual(res1,res2)

    def test_bad_registration(self):
        result1 = self.service.register("", "password")
        self.assertIsNotNone(result1)


if __name__ == '__main__':
    unittest.main()
