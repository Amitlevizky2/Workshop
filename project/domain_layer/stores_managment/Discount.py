from abc import ABC, abstractmethod
from datetime import date


class Discount(ABC):
    _ID = 0

    def __init__(self, start_date, end_date, percent):
        self.id = self._ID
        self.__class__._ID += 1
        self.start = start_date
        self.end = end_date
        self.discount = 1 - percent / 100

    @abstractmethod
    def commit_discount(self, original_price, amount):
        pass

    @abstractmethod
    def edit_discount(self):
        pass

    def is_valid_start_date(self, _date):
        return _date > date.today()

    def is_valid_end_date(self, end_date):
        return end_date > self.start and end_date > date.today()

    def is_valid_percent(self, percent):
        return 0 < percent < 100


class VisibleProductDiscount(Discount):
    def __init__(self, start_date, end_date, percent):
        super().__init__(start_date, end_date, percent)

    def commit_discount(self, original_price, amount):
        price_after_discount = original_price * self.discount
        return price_after_discount

    def edit_discount(self, start_date=None, end_date=None, percent=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and is_valid_start_date(start_date):
            self.start = start_date
        if end_date is not None and is_valid_end_date(end_date):
            self.end = end_date
        if percent is not None and is_valid_percent(percent):
            self.discount = 1 - percent / 100

    def is_valid_start_date(self, _date):
        super().is_valid_start_date(_date)

    def is_valid_end_date(self, end_date):
        super().is_valid_end_date(end_date)

    def is_valid_percent(self, percent):
        super().is_valid_percent(percent)


class ConditionalProductDiscount(Discount):
    def __init__(self, start_date, end_date, percent, discount_condition):
        super().__init__(start_date, end_date, percent)
        self.discount_condition = discount_condition

    def commit_discount(self, original_price, amount):
        num_prods_to_red = int(amount / self.discount_condition.amount_to_apply)
        return num_prods_to_red*((1-self.discount_condition.percent)*original_price)

    def edit_discount(self, start_date=None, end_date=None, percent=None, discount_condition=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and is_valid_start_date(start_date):
            self.start = start_date
        if end_date is not None and is_valid_end_date(end_date):
            self.end = end_date
        if percent is not None and is_valid_percent(percent):
            self.discount = 1 - percent / 100
        if discount_condition is not None and self.is_valid_condition(discount_condition):
            self.discount_condition = discount_condition

    def is_valid_condition(self, discount_conditions):
        return discount_conditions[0] > 0 and 0 <= discount_conditions <= 100


class ConditionalStoreDiscount(Discount):
    def __init__(self, start_date, end_date, percent, discount_conditions):
        super().__init__(start_date, end_date, percent)
        self.discount_conditions = discount_conditions

    def commit_discount(self, original_price, amount):
        pass

    def edit_discount(self, start_date=None, end_date=None, percent=None, discount_conditions=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and is_valid_start_date(start_date):
            self.start = start_date
        if end_date is not None and is_valid_end_date(end_date):
            self.end = end_date
        if percent is not None and is_valid_percent(percent):
            self.discount = 1 - percent / 100
        if discount_conditions is not None:
            self.discount_conditions.append(discount_conditions)

