from unittest import TestCase

from project.data_access_layer import proxy, session



class TestCart(TestCase):
    def setUp(self) -> None:
        self.proxy = proxy

    def test_real_proxy(self):
        sess = session
        self.assertEqual(self.proxy.get_session(), sess)

    def test_fail_proxy(self):
        proxy.session = False
        try:
            proxy.get_session()
        except:
            proxy.session = session
            self.assertTrue(True)
