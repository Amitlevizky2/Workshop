#import Bridge, Proxy
from Proxy import Proxy
from Bridge import Bridge

class Driver:
    def main(self):
        print(issubclass(Proxy, Bridge))

    @staticmethod
    def  make_bridge():
        proxy = Proxy()
        # adapter = Adapter()
        # proxy.setReal(adapter)
        return proxy

if __name__ == "__main__":
    d = Driver()
    d.main()

