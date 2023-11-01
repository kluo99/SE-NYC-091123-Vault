class Transaction:
    counter, catalog = 0, []

    def __init__(self, customer, coffee, price):
        self.customer = customer
        self.coffee = coffee
        self.price = price

        Transaction.counter += 1
        Transaction.catalog.append(self)

        coffee.access_current_transactions(self)
        coffee.access_current_customers(customer)
        
        customer.access_current_transactions(self)
        customer.access_current_coffees(coffee)

    def __repr__(self):
        return f"{self.customer.name} ordered a {self.coffee.name} for ${self.price}."

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        PRICE_IS_NUMERICAL = (type(price) in (int, float))
        PRICE_WITHIN_ACCEPTABLE_RANGE = (1 <= price <= 50)
        if PRICE_IS_NUMERICAL and PRICE_WITHIN_ACCEPTABLE_RANGE:
            self._price = price
        else:
            raise Exception("Unacceptable data format for `Transaction.price`!")

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, customer):
        from classes.customer import Customer
        CUSTOMER_TYPE_IS_VALID = isinstance(customer, Customer)
        if CUSTOMER_TYPE_IS_VALID:
            self._customer = customer
        else:
            raise Exception("Unacceptable data type for `Transaction.customer`!")

    @property
    def coffee(self):
        return self._coffee

    @coffee.setter
    def coffee(self, coffee):
        from classes.coffee import Coffee
        COFFEE_TYPE_IS_VALID = isinstance(coffee, Coffee)
        if COFFEE_TYPE_IS_VALID:
            self._coffee = coffee
        else:
            raise Exception("Unacceptable data type for `Transaction.coffee`!")