from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.PurchasesPolicies.PurchasePolicy import PurchasePolicy


class PurchaseCompositePolicy(PurchasePolicy):
    def __init__(self, purchase_policies: list, logic_operator: LogicOperator, id: int):
        super().__init__()
        self.logic_operator = logic_operator
        self.purchase_policies = purchase_policies
        self.id = id
        self.purchase_type = "Purchase Composite Policy"

    def is_approved(self, product_price_dict: dict):
        outcome_description = ""
        is_approved = True

        if self.logic_operator == LogicOperator.AND:
            is_approved, outcome_description = self.is_approved_and(product_price_dict)
        elif self.logic_operator == LogicOperator.OR:
            is_approved, outcome_description = self.is_approved_or(product_price_dict)
        elif self.logic_operator == LogicOperator.XOR:
            is_approved, outcome_description = self.is_approved_xor(product_price_dict)

        return is_approved, outcome_description

    def add_policy(self, purchase_policy):
        self.purchase_policies.append(purchase_policy)

    def remove_policy(self, purchase_policy):
        if purchase_policy in self.purchase_policies:
            self.purchase_policies.remove(purchase_policy)

    def is_approved_and(self, product_price_dict: dict):
        outcome_description = ""
        is_approved = True

        for purchase_policy in self.purchase_policies:
            p_is_approved, temp_desc = purchase_policy.is_approved(product_price_dict)

            if p_is_approved:
                outcome_description = outcome_description + " " + str(
                    purchase_policy.id) + " Policy approved\n"
            else:
                outcome_description = outcome_description + " " + str(
                    purchase_policy.id) + " Policy not approved\n"

            is_approved = is_approved and p_is_approved
            outcome_description = outcome_description + temp_desc
        return is_approved, outcome_description

    def is_approved_or(self, product_price_dict: dict):
        outcome_description = ""
        is_approved = True

        for purchase_policy in self.purchase_policies:
            p_is_approved, temp_desc = purchase_policy.is_approved(product_price_dict)

            if p_is_approved:
                outcome_description = outcome_description + " " + str(
                    purchase_policy.id) + " Policy approved\n"
            else:
                outcome_description = outcome_description + " " + str(
                    purchase_policy.id) + " Policy not approved\n"

            is_approved = is_approved or p_is_approved
            outcome_description = outcome_description + temp_desc
        return is_approved, outcome_description

    def is_approved_xor(self, product_price_dict: dict):
        outcome_description = ""
        is_first_true = False
        is_approved = False

        for purchase_policy in self.purchase_policies:
            p_is_approved, temp_description = purchase_policy.is_approved(product_price_dict)

            if is_first_true and p_is_approved:
                outcome_description = outcome_description + " " + str(
                    purchase_policy.id) + " Not First Policy that approved\n"
                is_approved = False

            elif not is_first_true and p_is_approved:
                outcome_description = outcome_description + " " + str(purchase_policy.id) + " First Policy that approved\n"
                is_first_true = True
                is_approved = True

            outcome_description = outcome_description + temp_description
        return is_approved, outcome_description

    def get_type(self):
        return self.purchase_type
