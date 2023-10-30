class Transaction:
    counter, catalog = 0, []

    def __init__(self, customer, coffee, price):
        self.customer = customer
        self.coffee = coffee
        self.price = price

        Transaction.counter += 1
        Transaction.catalog.append(self)

    def __repr__(self):
        return f"{self.customer.name} ordered a {self.coffee.name} for ${self.price}."