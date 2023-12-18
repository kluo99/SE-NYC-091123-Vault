class Coffee:
    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.customers = []


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and not hasattr(self, "name"):
            self._name = name
        else:
            raise Exception("error")

    def __repr__(self):
        return f"Coffee: {self.name}"

    def access_current_transactions(self, new_transaction=None):
        from classes.transaction import Transaction
        if new_transaction and isinstance(new_transaction, Transaction):
            self.transactions.append(new_transaction)
        return self.transactions


    def access_current_customers(self, new_customer=None):
        from classes.customer import Customer
        if isinstance(new_customer, Customer) and new_customer not in self.customers:
            self.customers.append(new_customer)
        return list(self.customers)

    def calculate_total_number_of_transactions(self):
        return len(self.transactions)
    
    def calculate_average_price_across_all_transactions(self):
        total_price = 0
        for transaction in self.transactions:
            total_price += transaction.price
        return total_price / self.calculate_total_number_of_transactions()