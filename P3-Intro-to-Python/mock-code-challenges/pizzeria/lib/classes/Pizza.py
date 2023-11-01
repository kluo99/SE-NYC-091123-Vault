class Pizza:
    def __init__(self, name):
        self.name = name
        self.orders = []
        self.customers = []

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

    def access_current_orders(self, new_order=None):
        from classes.order import Order
        ORDER_ALREADY_CREATED = (new_order is not None)
        ORDER_TYPE_IS_VALID = isinstance(new_order, Order)
        if ORDER_ALREADY_CREATED and ORDER_TYPE_IS_VALID:
            self.orders.append(new_order)
        return self.orders

    def access_current_customers(self, new_customer=None):
        from classes.customer import Customer
        CUSTOMER_IS_UNIQUE = (new_customer not in self.customers)
        CUSTOMER_TYPE_IS_VALID = isinstance(new_customer, Customer)
        if CUSTOMER_IS_UNIQUE and CUSTOMER_TYPE_IS_VALID:
            self.customers.append(new_customer)
        return self.customers

    def calculate_total_number_of_orders(self):
        return len(self.orders)
    
    def calculate_average_price_across_all_orders(self):
        total_price = 0
        for order in self.orders:
            total_price += order.price
        return total_price / self.calculate_total_number_of_orders()