import unittest
from Driver import Driver
from User import User

service = Driver.make_bridge()
username1 = "avi"
password1 = 123
username2 = "beni"
password2 = 321


class MyTestCase(unittest.TestCase):



    def test_happy_registration(self):
        result1 = service.register(username1,password1)
        result2 = service.register(username2,password1)
        self.assertNotEqual(result1,result2)

    def test_sad_registration(self):
        result1 = service.register(username1,password1)
        result2 = service.register(username1,password2)
        self.assertFalse(result1)

    def test_bad_registration(self):
        result1 = service.register("",password1)
        self.assertFalse(result1)


if __name__ == '__main__':
    unittest.main()
