
from project.tests.AT_tests.test_env.Proxy import Proxy


class Driver:
    def main(self):pass

    @staticmethod
    def  make_bridge():
        proxy = Proxy()
    # adapter = Adapter()
    # proxy.setReal(adapter)
        return proxy


if __name__ == "__main__":
    d = Driver()
    d.main()

