import pytest

from classes.pizza import Pizza
from classes.customer import Customer
from classes.order import Order

class TestOrders:
    '''Order in order.py'''

    def test_has_price(self):
        ''' Tests that an order is initialized with a numerical price. '''
        pizza = Pizza("Cheese")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (order_1.price == 2)
        assert (order_2.price == 5)

    def test_has_a_customer(self):
        ''' Tests that an order has a customer.'''
        pizza = Pizza("Cheese")
        customer_1 = Customer('Wayne')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_2, pizza, 5)

        assert (order_1.customer == customer_1)
        assert (order_2.customer == customer_2)

    def test_customer_of_type_customer(self):
        ''' Tests that an order's customer is of type `Customer`. '''
        pizza = Pizza("Mushroom")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (isinstance(order_1.customer, Customer))
        assert (isinstance(order_2.customer, Customer))

    def test_has_a_pizza(self):
        ''' Tests that an order has a pizza. '''
        pizza_1 = Pizza("Cheese")
        pizza_2 = Pizza("Pepperoni")
        customer = Customer('Wayne')
        order_1 = Order(customer, pizza_1, 2)
        order_2 = Order(customer, pizza_2, 5)

        assert (order_1.pizza == pizza_1)
        assert (order_2.pizza == pizza_2)

    def test_pizza_of_type_pizza(self):
        ''' Tests that an order's pizza is of type `Pizza`. '''
        pizza = Pizza("Mushroom")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (isinstance(order_1.pizza, Pizza))
        assert (isinstance(order_2.pizza, Pizza))

    def test_get_all_orders(self):
        ''' Tests that the `Order` class is tracking all current instances in a list attribute. '''
        Order.catalog = []
        pizza = Pizza("Cheese")
        customer = Customer('Wayne')
        customer_2 = Customer('Dima')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer_2, pizza, 5)

        assert (len(Order.catalog) == 2)
        assert (order_1 in Order.catalog)
        assert (order_2 in Order.catalog)