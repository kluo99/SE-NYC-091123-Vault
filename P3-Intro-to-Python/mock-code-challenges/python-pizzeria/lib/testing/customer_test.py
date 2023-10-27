import pytest

from classes.pizza import Pizza
from classes.customer import Customer
from classes.order import Order

class TestCustomer:
    '''Customer in customer.py'''

    def test_has_name(self):
        '''customer is initialized with name'''
        customer = Customer('Steve')
        assert (customer.name == "Steve")

    def test_can_change_name(self):
        '''customer name can be changed'''
        customer = Customer('Steve')
        customer.name = "Stove"
        assert (customer.name == "Stove")

    def test_customer_name_is_str(self):
        '''customer name is a string'''
        customer = Customer('Steve')
        assert (isinstance(customer.name, str))

        with pytest.raises(Exception):
            customer.name = 1

    def test_customer_name_length(self):
        '''customer name is between 1 and 15 characters'''
        customer = Customer('Steve')
        assert (len(customer.name) == 5)

        with pytest.raises(Exception):
            customer.name = "NameLongerThan15Characters"

        with pytest.raises(Exception):
            customer.name = ""

    def test_has_many_orders(self):
        '''customer has many orders'''
        pizza = Pizza("Cheese")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_1, pizza, 5)
        order_3 = Order(customer_2, pizza, 5)

        assert (len(customer_1.orders()) == 2)
        assert (not order_3 in customer_1.orders())
        assert (order_1 in customer_1.orders())
        assert (order_2 in customer_1.orders())

    def test_orders_of_type_order(self):
        '''customer orders are of type Order'''
        pizza = Pizza("Cheese")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (isinstance(customer.orders()[0], Order))
        assert (isinstance(customer.orders()[1], Order))

    def test_has_many_pizzas(self):
        '''customer has many pizzas.'''
        pizza_1 = Pizza("Cheese")
        pizza_2 = Pizza("Mushroom")

        customer = Customer('Steve')
        order_1 = Order(customer, pizza_1, 2)
        order_2 = Order(customer, pizza_2, 5)

        assert (pizza_1 in customer.pizzas())
        assert (pizza_2 in customer.pizzas())

    def test_has_unique_pizzas(self):
        '''customer has unique list of all the pizzas they have ordered.'''
        pizza_1 = Pizza("Cheese")
        pizza_2 = Pizza("Mushroom")

        customer = Customer('Steve')
        order_1 = Order(customer, pizza_1, 2)
        order_2 = Order(customer, pizza_1, 2)
        order_3 = Order(customer, pizza_2, 5)

        assert (len(set(customer.pizzas())) == len(customer.pizzas()))
        assert (len(customer.pizzas()) == 2)