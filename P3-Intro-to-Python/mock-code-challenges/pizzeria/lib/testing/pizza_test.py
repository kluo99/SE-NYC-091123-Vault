import pytest

from classes.pizza import Pizza
from classes.customer import Customer
from classes.order import Order

class TestPizza:
    '''  Testing class for assessing quality of `pizza.Pizza` object. '''

    def test_has_name(self):
        ''' Tests that a pizza is initialized with a name. '''
        pizza = Pizza("Cheese")
        assert (pizza.name == "Cheese")

    def test_name_is_string(self):
        ''' Tests that a pizza's name is a string. '''
        pizza = Pizza("Cheese")
        assert (isinstance(pizza.name, str))

    def test_name_setter(self):
        ''' Tests that a pizza's name cannot change after initialization. '''
        pizza = Pizza("Cheese")

        with pytest.raises(Exception):
            pizza.name = "Pepperoni"

    def test_has_many_orders(self):
        ''' Tests that a pizza can have many orders. '''
        pizza_1 = Pizza("Sicilian")
        pizza_2 = Pizza("Mushroom")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza_1, 2)
        order_2 = Order(customer, pizza_1, 5)
        order_3 = Order(customer, pizza_2, 5)

        assert (len(pizza_1.access_current_orders()) == 2)
        assert (order_1 in pizza_1.access_current_orders())
        assert (order_2 in pizza_1.access_current_orders())
        assert (not order_3 in pizza_1.access_current_orders())

    def test_orders_of_type_order(self):
        ''' Tests that a pizza's orders are each of type `Order`. '''
        pizza = Pizza("Meat Lovers")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (isinstance(pizza.access_current_orders()[0], Order))
        assert (isinstance(pizza.access_current_orders()[1], Order))

    def test_has_many_customers(self):
        ''' Tests that a pizza can have many customers. '''
        pizza = Pizza("Grandma")

        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_2, pizza, 5)

        assert (customer_1 in pizza.access_current_customers())
        assert (customer_2 in pizza.access_current_customers())

    def test_has_unique_customers(self):
        ''' Tests that a pizza has a unique list of all the customers that have ordered it. '''
        pizza = Pizza("Grandma")

        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_2, pizza, 2)
        order_3 = Order(customer_1, pizza, 5)

        assert (len(set(pizza.access_current_customers())) == len(pizza.access_current_customers()))
        assert (len(pizza.access_current_customers()) == 2)

    def test_customers_of_type_customer(self):
        ''' Tests that a pizza's customers are each of type `Customer`. '''
        pizza = Pizza("Grandma")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        order_1 = Order(customer_1, pizza, 2)
        order_2 = Order(customer_2, pizza, 5)

        assert (isinstance(pizza.access_current_customers()[0], Customer))
        assert (isinstance(pizza.access_current_customers()[1], Customer))

    def test_get_total_number_of_orders(self):
        ''' Tests that the number of total orders for a given pizza can be calculated. '''
        pizza = Pizza("Cheese")
        customer = Customer('Steve')
        order_1 = Order(customer, pizza, 2)
        order_2 = Order(customer, pizza, 5)

        assert (pizza.calculate_total_number_of_orders() == 2)

    def test_average_price(self):
        ''' Tests that the average price for a given pizza across all orders can be calculated. '''
        pizza = Pizza("Cheese")
        customer = Customer('Steve')
        customer_2 = Customer('Dima')
        Order(customer, pizza, 2)
        Order(customer_2, pizza, 5)

        assert (pizza.calculate_average_price_across_all_orders() == 3.5)