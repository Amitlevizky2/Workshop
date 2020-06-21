from project.tests.AT_tests.test_env.Proxy import Proxy
from project.tests.AT_tests.test_env.Adapter import Adapter

class Driver:
    def main(self): pass

    @staticmethod
    def make_bridge() -> Proxy:
        proxy = Proxy()
        #adapter = Adapter()
        #proxy.set_real(adapter)
        return proxy


if __name__ == "__main__":
    d = Driver()
    d.main()
