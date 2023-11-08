class Coffee:
    def __init__(self, name):
        self.name = name
        self.customers = []
        self.transactions = []

    def __repr__(self):
        return f"Coffee: {self.name}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        NAME_IS_STR = isinstance(name, str)
        NAME_EXISTS = (not hasattr(self, "name"))
        if NAME_IS_STR and NAME_EXISTS:
            self._name = name
        else:
            raise Exception("`Pizza.name` already exists!")

    def access_current_transactions(self, new_transaction=None):
        from classes.transaction import Transaction
        TRANSACTION_ALREADY_CREATED = (new_transaction is not None)
        TRANSACTION_TYPE_IS_VALID = isinstance(new_transaction, Transaction)
        if TRANSACTION_ALREADY_CREATED and TRANSACTION_TYPE_IS_VALID:
            self.transactions.append(new_transaction)
        return self.transactions

    def access_current_customers(self, new_customer=None):
        from classes.customer import Customer
        CUSTOMER_IS_UNIQUE = (new_customer not in self.customers)
        CUSTOMER_TYPE_IS_VALID = isinstance(new_customer, Customer)
        if CUSTOMER_IS_UNIQUE and CUSTOMER_TYPE_IS_VALID:
            self.customers.append(new_customer)
        return self.customers
    
    def calculate_total_number_of_transactions(self):
        return len(self.transactions)
    
    def calculate_average_price_across_all_transactions(self):
        total_price = 0
        for transaction in self.transactions:
            total_price += transaction.price
        return total_price / self.calculate_total_number_of_transactions()