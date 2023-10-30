class Order:
    catalog = []

    def __init__(self, customer, pizza, price):
        self.customer = customer
        self.pizza = pizza
        self.price = price

        Order.catalog.append(self)

    def __repr__(self):
        return f"{self.customer.name} ordered a {self.pizza.name} for ${self.price}."