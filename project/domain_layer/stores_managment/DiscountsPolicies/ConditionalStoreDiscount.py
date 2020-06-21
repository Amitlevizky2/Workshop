import datetime
from datetime import datetime
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from project.domain_layer.stores_managment.Product import Product


class ConditionalStoreDiscount(Discount):
    def __init__(self, start_date, end_date, percent, min_price, store_id, orm=None):
        super().__init__(start_date, end_date, percent, store_id)
        # self.products_in_discount = {}  # {product_name: bool}
        self.min_price = min_price
        self.orm = orm
        self.discount_type = "Conditional Store Discount"

    def commit_discount(self, product_price_dict: dict):
        total_basket_price = self.basket_total_price(product_price_dict)
        if self.start < datetime.today() < self.end and total_basket_price >= self.min_price:
            to_add_discount = "Store Discount" + str(self.id)
            price = self.calculate_conditional_discount(total_basket_price)
            discount_as_product = Product(to_add_discount, (-price), "none", "none", 1)
            new_product_tup = (discount_as_product, 1,
                               price, price)

            product_price_dict[to_add_discount] = new_product_tup
            x = 5

    def get_product_object(self, product):
        return product[0]

    def get_product_amount(self, product):
        return product[1]

    def get_product_updated_price(self, product):
        new_price = product[2] - self.calculate_conditional_discount()
        return new_price

    def calculate_conditional_discount(self, total_basket_price):
        return total_basket_price * self.discount

    #  {product_name, (Product, amount, updated_price, original_price)}
    def basket_total_price(self, product_price_dict: dict):
        total_amount = 0
        for product_tup in product_price_dict.values():
            total_amount += self.get_product_amount(product_tup) * self.get_product_object(product_tup).original_price
        return total_amount

    def edit_discount(self, start_date, end_date, percent, min_price):
        is_edited = False
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and start_date > datetime.today():
            self.start = start_date
            self.orm.update_start(start_date)
            is_edited = True
        if end_date is not None and end_date > self.start and end_date > datetime.today():
            self.end = end_date
            self.orm.update_end(end_date)
            is_edited = True
        if percent is not None and 0 <= percent <= 100:
            self.discount = percent / 100
            self.orm.update_prcent(self.discount)
            is_edited = True
        if min_price is not None and 0 < min_price:
            self.min_price = min_price
            self.orm.Update_min_price(min_price)
            is_edited = True

        return is_edited

    def is_in_discount(self, product_name: str, product_price_dict: dict):
        return self.basket_total_price(product_price_dict) > self.min_price and self.start < datetime.today() < self.end

    def get_discount_type(self):
        return self.discount_type

    def get_description(self):
        return [self.id, self.discount_type, self.start, self.end, self.discount, self.min_price]

    def get_updated_price(self, product: Product):
        return product.original_price

    def get_jsn_description(self):
        return {"Start Date": self.start.strftime('%m/%d/%Y'),
                "End Date": self.end.strftime('%m/%d/%Y'),
                "Percent": self.discount,
                "Min price": self.min_price,
                "Products In Discount": self.products_in_discount.keys(),
                "Discount Type": self.discount_type}

    def is_approved(self, original_price, amount):
        pass

    def createORM(self):
        if self.orm is None:
            from project.data_access_layer.ConditionalStoreDiscountORM import ConditionalStoreDiscountsORM
            self.orm = ConditionalStoreDiscountsORM()
            self.orm.discount_id= self.id
            self.orm.store_id = self.store_id
            self.orm.start_date = self.start
            self.orm.end_date = self.end
            self.orm.percent = self.discount
            self.orm.min_price = self.min_price
            for prod in self.products_in_discount.keys():
                from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM
                pidorm = ProductsInDiscountsORM(discount_id=self.discount_id, product_name=prod, store_id=self.store_id)
                pidorm.add()
            self.orm.add()