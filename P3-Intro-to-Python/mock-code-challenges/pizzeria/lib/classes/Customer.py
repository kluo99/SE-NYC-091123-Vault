class Customer:
    def __init__(self, name):
        self.name = name
        
    def orders(self, new_order=None):
        from classes.order import Order
        pass
    
    def pizzas(self, new_pizza=None):
        from classes.pizza import Pizza
        pass