class Customer:
    def __init__(self, name):
        self.name = name
        self.coffees = []
        self.transactions = []

    def __repr__(self):
        return f"Customer: {self.name}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        NAME_IS_STR = isinstance(name, str)
        NAME_WITHIN_ACCEPTABLE_LENGTH = (1 <= len(name) <= 15)
        if NAME_IS_STR and NAME_WITHIN_ACCEPTABLE_LENGTH:
            self._name = name
        else:
            raise Exception("Unacceptable data format for `Customer.name`!")

    def access_current_transactions(self, new_transaction=None):
        from classes.transaction import Transaction
        TRANSACTION_ALREADY_CREATED = (new_transaction is not None)
        TRANSACTION_TYPE_IS_VALID = isinstance(new_transaction, Transaction)
        if TRANSACTION_ALREADY_CREATED and TRANSACTION_TYPE_IS_VALID:
            self.transactions.append(new_transaction)
        return self.transactions

    def access_current_coffees(self, new_coffee=None):
        from classes.coffee import Coffee
        COFFEE_ALREADY_CREATED = (new_coffee is not None)
        COFFEE_TYPE_IS_VALID = isinstance(new_coffee, Coffee)
        COFFEE_IS_UNIQUE = (new_coffee not in self.coffees)
        if COFFEE_ALREADY_CREATED and COFFEE_TYPE_IS_VALID and COFFEE_IS_UNIQUE:
            self.coffees.append(new_coffee)
        return self.coffees
    
    def place_order(self, name_of_coffee, price):
        from classes.coffee import Coffee
        from classes.transaction import Transaction
        return Transaction(self, Coffee(name_of_coffee), price)

    def calculate_total_money_spent(self):
        return sum(transaction.price for transaction in self.transactions)
    
    def retrieve_coffees_within_price_range(self, min_price=0, max_price=999):
        filtered_coffees = []
        for transaction in self.transactions:
            if min_price <= transaction.price <= max_price:
                filtered_coffees.append(transaction.coffee)
        return filtered_coffees