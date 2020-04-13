class Basket:
    # send the initial product to init????
    def __init__(self, store_id):
        # products = {"product name",(Product,amount)}
        self.products = {}
        self.store_id = store_id
        self.total = 0

    # NOT SURE IF THE FUNCTION WORKS
    #NEED TO DECIDE IF HOLD PRODUCT OR NAME HOW TO GET PRICE IF NAME
    def get_total(self):
        total = 0
        for product in self.products.keys():
            total += product.price * (self.products.get(product))
        self.total = total
        return self.total