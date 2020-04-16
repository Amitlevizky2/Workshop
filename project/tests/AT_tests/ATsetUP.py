from project.tests.AT_tests.test_env import Proxy

products = [("Apple", 20, "Food", "Fruits", 10),
            ("Banana", 20, "Food", "Fruits", 10),
            ("Orange", 20, "Food", "Fruits", 10),
            ("Tomato", 20, "Food", "Vegetables", 10),
            ("Cucumber", 20, "Food", "Vegetables", 10),
            ("Carrot", 20, "Food", "Vegetables", 10),
            ("Iphone", 20, "Electronics", "Computers", 10),
            ("Hard Disk", 20, "Electronics", "Computers", 10),
            ("Keyboard", 20, "Electronics", "Computers", 10)]


def setup(service: Proxy):
    service.register("avi", "123")
    service.login("avi", "123")
    store_id = service.Open_store("avishop")
    for product in products:
        service.add_product_to_Store(store_id, *product)
    return store_id

