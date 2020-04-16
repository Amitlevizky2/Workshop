import unittest
from Driver import Driver

service = Driver.make_bridge()
username1 = "avi"
password1 = 123
username2 = "beni"
password2 = 321

class login(unittest.TestCase):
    def test_happy_registration(self):
        service.register(username1, password1)
        result1 = service.login(username1, password1)
        self.assertTrue(result1, service.login(username1, password1))

    def test_sad_registration(self):
        service.register(username2, password2)
        result1 = service.login(username2, password2)
        self.assertFalse(result1, service.login(username2, password1))

    def test_bad_registration(self):
        service.register(username2, password2)
        result1 = service.login(username2, password2)
        self.assertFalse(result1, service.login(None, None))