from datetime import date, datetime

from project.domain_layer.stores_managment import Product
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount


class CompositeDiscount(Discount):                                    #[(Discount, [products_name])]
    def __init__(self, start_date, end_date, logic_operator: LogicOperator, cond_prod_tup_list: list, discounts_to_apply: list, store_id, orm=None):
        super().__init__(start_date, end_date, 0, store_id)
        self.discounts_to_apply = discounts_to_apply
        self.logic_operator = logic_operator
        # self.products_in_discount = {}  # {product: bool}
        self.cond_prod_tup_list = cond_prod_tup_list
        self.orm = orm
        self.discount_type = "Composite Discount"

    def commit_discount(self, product_price_dict: dict):
        if self.start < datetime.today() < self.end:
            is_valid = True
            if self.logic_operator == LogicOperator.AND:
                is_valid = self.check_and_operator(product_price_dict)
            elif self.logic_operator == LogicOperator.OR:
                is_valid = self.check_or_operator(product_price_dict)
            elif self.logic_operator == LogicOperator.XOR:
                is_valid = self.check_xor_operator(product_price_dict)

            if is_valid:
                for discount in self.discounts_to_apply:
                    discount.commit_discount(product_price_dict)

    def check_and_operator(self, product_price_dict):
        is_valid = True
        for tupel in self.cond_prod_tup_list:
            is_valid = is_valid and self.is_valid_cond_prod_tup(tupel, product_price_dict)
        return is_valid

    def check_or_operator(self, product_price_dict):
        is_valid = False
        for tupel in self.cond_prod_tup_list:
            is_valid = is_valid or self.is_valid_cond_prod_tup(tupel, product_price_dict)
        return is_valid

    def is_in_discount(self, product_name: str, product_price_dict):
        pass

    def check_xor_operator(self, product_price_dict):
        is_valid = False
        for tupel in self.cond_prod_tup_list:
            if self.is_valid_cond_prod_tup(tupel, product_price_dict):
                is_valid = not is_valid
        return is_valid

    def is_valid_cond_prod_tup(self, tupel, product_price_dict):
        discount: Discount = tupel[0]
        is_valid = True

        for product_name in tupel[1]:
            if not discount.is_in_discount(product_name, product_price_dict):
                is_valid = False

        return is_valid

    def is_approved(self, original_price, amount):
        pass

    def edit_discount(self):
        pass

    def get_discount_type(self):
        return self.discount_type

    def get_description(self):
        discounts_to_apply_description = []
        for discount in self.discounts_to_apply:
            discounts_to_apply_description.append(discount.get_description())

        discount_to_check_and_products_description = {}
        for tup in self.cond_prod_tup_list:
            discount_to_check_and_products_description[tup[0].id] = tup[1]

        return [self.id, self.discount_type, self.start, self.end, self.logic_operator, discount_to_check_and_products_description, discounts_to_apply_description]

    def get_jsn_description(self):
        discounts_to_apply_description = []
        for discount in self.discounts_to_apply:
            discounts_to_apply_description.append(discount.get_jsn_description())

        discount_to_check_and_products_description = {}
        for tup in self.cond_prod_tup_list:
            discount_to_check_and_products_description[tup[0].id] = tup[1]

        return {"Start Date": self.start.strftime('%m/%d/%Y'),
                "End Date": self.end.strftime('%m/%d/%Y'),
                "Logic Operator": self.logic_operator.__str__(),
                "Discounts to apply description": discounts_to_apply_description,
                "Discount to check and products description": discount_to_check_and_products_description,
                "Products In Discount": self.products_in_discount.keys(),
                "Discount Type": self.discount_type}

    def get_updated_price(self, product: Product):
        return product.original_price

    def createORM(self):
        #TODO: add building of list of predicates and to_apply
        if self.orm is None:
            from project.data_access_layer.CompositeDiscountORM import CompositeDiscountORM
            self.orm = CompositeDiscountORM()
            self.orm.discount_id= self.id
            self.orm.start_date = self.start
            self.orm.end_date = self.end
            self.orm.percent = self.discount
            self.orm.logic_operator = self.logic_operator
            for prod in self.products_in_discount.keys():
                from project.data_access_layer.ProductsInDiscountsORM import ProductsInDiscountsORM
                pidorm = ProductsInDiscountsORM(discount_id=self.discount_id, product_name=prod, store_id=self.store_id)
                pidorm.add()
            self.orm.add()