class Coffee:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Coffee: {self.name}"

    def access_current_transactions(self, new_transaction=None):
        from classes.transaction import Transaction
        pass

    def access_current_customers(self, new_customer=None):
        from classes.customer import Customer
        pass

    def calculate_total_number_of_transactions(self):
        pass
    
    def calculate_average_price_across_all_transactions(self):
        pass