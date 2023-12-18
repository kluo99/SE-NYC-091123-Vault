from classes.customer import Customer
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

    @property
    def price(self):
        return self._price

    @price.setter 
    def price(self, price):
        if (1 <= price <= 50):
            self._price = price
        else:
            raise Exception("error")
    
    @property
    def customer(self):
        return self._customer
    
    @customer.setter
    def customer(self, customer):
        if isinstance(customer, Customer):
            self._customer = customer
        else:
            raise Exception('error')
    
    @property
    def coffee(self):
        return self._coffee  

    @coffee.setter
    def coffee(self, coffee):
        from classes.coffee import Coffee
        if isinstance(coffee, Coffee):
            self._coffee = coffee
        else:
            raise Exception("error")
    

        

    def __repr__(self):
        return f"{self.customer.name} ordered a {self.coffee.name} for ${self.price}."