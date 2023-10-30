import pytest

from classes.pizza import Pizza
from classes.customer import Customer
from classes.order import Order

class TestCustomer:
    ''' Testing class for assessing quality of `customer.Customer` object. '''

    def test_has_name(self):
        ''' Tests that a customer is initialized with a name. '''
        customer = Customer('Steve')
        assert (customer.name == "Steve")

    def test_can_change_name(self):
        ''' Tests that a customer's name can be changed after initialization. '''
        customer = Customer('Steve')
        customer.name = "Stove"
        assert (customer.name == "Stove")

    def test_customer_name_is_str(self):
        ''' Tests that a customer's name is a string. '''
        customer = Customer('Steve')
        assert (isinstance(customer.name, str))

        with pytest.raises(Exception):
            customer.name = 1

    def test_customer_name_length(self):
        ''' Tests that a customer's name is between 1 and 15 characters. '''
        customer = Customer('Steve')
        assert (len(customer.name) == 5)

        with pytest.raises(Exception):
            customer.name = "NameLongerThan15Characters"

        with pytest.raises(Exception):
            customer.name = ""

    def test_has_many_orders(self):
        ''' Tests that a customer can have many orders. '''
        pizza = Pizza("Cheese")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_1, pizza, 5)
        order_3 = Order(customer_2, pizza, 5)

        assert (len(customer_1.access_current_orders()) == 2)
        assert (not order_3 in customer_1.access_current_orders())
        assert (order_1 in customer_1.access_current_orders())
        assert (order_2 in customer_1.access_current_orders())

    def test_orders_of_type_order(self):
        ''' Tests that a customer's orders are each of type `Order`. '''
        pizza = Pizza("Cheese")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (isinstance(customer.access_current_orders()[0], Order))
        assert (isinstance(customer.access_current_orders()[1], Order))

    def test_has_many_pizzas(self):
        ''' Tests that a customer can have many pizzas. '''
        pizza_1 = Pizza("Cheese")
        pizza_2 = Pizza("Mushroom")

        customer = Customer('Steve')
        order_1 = Order(customer, pizza_1, 2)
        order_2 = Order(customer, pizza_2, 5)

        assert (pizza_1 in customer.access_current_pizzas())
        assert (pizza_2 in customer.access_current_pizzas())

    def test_has_unique_pizzas(self):
        ''' Tests that a customer has a unique list of all the pizzas that they have ordered. '''
        pizza_1 = Pizza("Cheese")
        pizza_2 = Pizza("Mushroom")

        customer = Customer('Steve')
        order_1 = Order(customer, pizza_1, 2)
        order_2 = Order(customer, pizza_1, 2)
        order_3 = Order(customer, pizza_2, 5)

        assert (len(set(customer.access_current_pizzas())) == len(customer.access_current_pizzas()))
        assert (len(customer.access_current_pizzas()) == 2)