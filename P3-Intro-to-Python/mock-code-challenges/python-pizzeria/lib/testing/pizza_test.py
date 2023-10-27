import pytest

from classes.pizza import Pizza
from classes.customer import Customer
from classes.order import Order

class TestPizza:
    '''Pizza in pizza.py'''

    def test_has_name(self):
        '''pizza is initialized with a name'''
        pizza = Pizza("Cheese")
        assert (pizza.name == "Cheese")

    def test_name_is_string(self):
        '''pizza is initialized with a name of type str'''
        pizza = Pizza("Cheese")
        assert (isinstance(pizza.name, str))

    def test_name_setter(self):
        '''Cannot change the name of the pizza'''
        pizza = Pizza("Cheese")

        with pytest.raises(Exception):
            pizza.name = "Pepperoni"

    def test_has_many_orders(self):
        '''pizza has many orders.'''
        pizza_1 = Pizza("Sicilian")
        pizza_2 = Pizza("Mushroom")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza_1, 2)
        order_2 = Order(customer, pizza_1, 5)
        order_3 = Order(customer, pizza_2, 5)

        assert (len(pizza_1.orders()) == 2)
        assert (order_1 in pizza_1.orders())
        assert (order_2 in pizza_1.orders())
        assert (not order_3 in pizza_1.orders())

    def test_orders_of_type_order(self):
        '''pizza orders are of type Order'''
        pizza = Pizza("Meat Lovers")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (isinstance(pizza.orders()[0], Order))
        assert (isinstance(pizza.orders()[1], Order))

    def test_has_many_customers(self):
        '''pizza has many customers.'''
        pizza = Pizza("Grandma")

        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_2, pizza, 5)

        assert (customer_1 in pizza.customers())
        assert (customer_2 in pizza.customers())

    def test_has_unique_customers(self):
        '''pizza has unique list of all the customers that have ordered it.'''
        pizza = Pizza("Grandma")

        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_2, pizza, 2)
        order_3 = Order(customer_1, pizza, 5)

        assert (len(set(pizza.customers())) == len(pizza.customers()))
        assert (len(pizza.customers()) == 2)

    def test_customers_of_type_customer(self):
        '''pizza customers are of type Customer'''
        pizza = Pizza("Grandma")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_2, pizza, 5)

        assert (isinstance(pizza.customers()[0], Customer))
        assert (isinstance(pizza.customers()[1], Customer))

    def test_get_number_of_orders(self):
        '''test num_orders()'''
        pizza = Pizza("Cheese")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (pizza.num_orders() == 2)

    def test_average_price(self):
        '''test average_price()'''
        pizza = Pizza("Cheese")
        customer = Customer('Steve')
        customer_2 = Customer('Dima')
        Order(customer, pizza, 2)
        Order(customer_2, pizza, 5)

        assert (pizza.average_price() == 3.5)