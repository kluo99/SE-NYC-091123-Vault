class Customer:    
    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.coffees = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and 1 <= len(name) <= 15:
            self._name = name
        else:
            raise Exception ('Must be a string')

    def __repr__(self):
        return f"Customer: {self.name}"

    def access_current_transactions(self, new_transaction=None):
        from classes.transaction import Transaction
        if new_transaction and isinstance(new_transaction, Transaction):
            self.transactions.append(new_transaction)
        return self.transactions

    def access_current_coffees(self, new_coffee=None):
        from classes.coffee import Coffee
        if isinstance(new_coffee, Coffee) and new_coffee not in self.coffees:
            self.coffees.append(new_coffee)
        return self.coffees


    def place_order(self, name_of_coffee, price):
        from classes.coffee import Coffee
        from classes.transaction import Transaction
        return Transaction(self, Coffee(name_of_coffee), price)

    def calculate_total_money_spent(self):
        return sum(transaction.price for transaction in self.transactions)
        pass
    
    def retrieve_coffees_within_price_range(self, min_price=0, max_price=999):
        filtered_coffees = []
        for transaction in self.transactions:
            if min_price <= transaction.price <= max_price:
                filtered_coffees.append(transaction.coffee)
        return filtered_coffees
        pass
