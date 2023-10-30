class Customer:
    def __init__(self, name):
        self.name = name

    def access_current_orders(self, new_order=None):
        from classes.order import Order
        pass

    def access_current_pizzas(self, new_pizza=None):
        from classes.pizza import Pizza
        pass