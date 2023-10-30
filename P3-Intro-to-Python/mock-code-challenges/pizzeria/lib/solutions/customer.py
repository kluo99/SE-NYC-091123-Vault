class Customer:
    def __init__(self, name):
        self.name = name
        self.orders = []
        self.pizzas = []

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

    def access_current_orders(self, new_order=None):
        from classes.order import Order
        ORDER_ALREADY_CREATED = (new_order is not None)
        ORDER_TYPE_IS_VALID = isinstance(new_order, Order)
        if ORDER_ALREADY_CREATED and ORDER_TYPE_IS_VALID:
            self.orders.append(new_order)
        return self.orders

    def access_current_pizzas(self, new_pizza=None):
        from classes.pizza import Pizza
        PIZZA_ALREADY_CREATED = (new_pizza is not None)
        PIZZA_TYPE_IS_VALID = isinstance(new_pizza, Pizza)
        PIZZA_IS_UNIQUE = (new_pizza not in self.pizzas)
        if PIZZA_ALREADY_CREATED and PIZZA_TYPE_IS_VALID and PIZZA_IS_UNIQUE:
            self.pizzas.append(new_pizza)
        return self.pizzas