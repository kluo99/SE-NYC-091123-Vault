class Customer:    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Customer: {self.name}"

    def access_current_transactions(self, new_transaction=None):
        from classes.transaction import Transaction
        pass

    def access_current_coffees(self, new_coffee=None):
        from classes.coffee import Coffee
        pass

    def place_order(self, name_of_coffee, price):
        pass

    def calculate_total_money_spent(self):
        pass
    
    def retrieve_coffees_within_price_range(self, min_price=0, max_price=999):
        pass