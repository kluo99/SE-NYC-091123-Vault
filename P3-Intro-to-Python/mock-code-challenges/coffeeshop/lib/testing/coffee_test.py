import pytest

from classes.coffee import Coffee
from classes.customer import Customer
from classes.transaction import Transaction

class TestCoffee:
    '''  Testing class for assessing stability of `coffee.Coffee` object. '''

    def test_has_name(self):
        ''' Tests that a coffee is initialized with a name. '''
        coffee = Coffee("Cappuccino")
        assert (coffee.name == "Cappuccino")

    def test_name_is_string(self):
        ''' Tests that a coffee's name is a string. '''
        coffee = Coffee("Cappuccino")
        assert (isinstance(coffee.name, str))

    def test_name_setter(self):
        ''' Tests that a coffee's name cannot change after initialization. '''
        coffee = Coffee("Cappuccino")

        with pytest.raises(Exception):
            coffee.name = "Espresso"

    def test_has_many_transactions(self):
        ''' Tests that a coffee can have many transactions. '''
        coffee_1 = Coffee("Espresso")
        coffee_2 = Coffee("Cappuccino")
        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee_1, 2)
        transaction_2 = Transaction(customer, coffee_1, 5)
        transaction_3 = Transaction(customer, coffee_2, 5)

        assert (len(coffee_1.access_current_transactions()) == 2)
        assert (transaction_1 in coffee_1.access_current_transactions())
        assert (transaction_2 in coffee_1.access_current_transactions())
        assert (not transaction_3 in coffee_1.access_current_transactions())

    def test_transactions_of_type_transaction(self):
        ''' Tests that a pizza's transactions are each of type `Transaction`. '''
        coffee = Coffee("Macchiatto")
        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee, 2)
        transaction_2 = Transaction(customer, coffee, 5)

        assert (isinstance(coffee.access_current_transactions()[0], Transaction))
        assert (isinstance(coffee.access_current_transactions()[1], Transaction))

    def test_has_many_customers(self):
        ''' Tests that a coffee can have many customers. '''
        coffee = Coffee("Macchiatto")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_2, coffee, 5)

        assert (customer_1 in coffee.access_current_customers())
        assert (customer_2 in coffee.access_current_customers())

    def test_has_unique_customers(self):
        ''' Tests that a coffee has a unique list of all the customers that have ordered it. '''
        coffee = Coffee("Macchiatto")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_2, coffee, 2)
        transaction_3 = Transaction(customer_1, coffee, 5)

        assert (len(set(coffee.access_current_customers())) == len(coffee.access_current_customers()))
        assert (len(coffee.access_current_customers()) == 2)

    def test_customers_of_type_customer(self):
        ''' Tests that a coffee's customers are each of type `Customer`. '''
        coffee = Coffee("Grandma")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_2, coffee, 5)

        assert (isinstance(coffee.access_current_customers()[0], Customer))
        assert (isinstance(coffee.access_current_customers()[1], Customer))

    def test_get_total_number_of_transactions(self):
        ''' Tests that the number of total transaction for a given coffee can be calculated. '''
        coffee = Coffee("Espresso")
        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee, 2)
        transaction_2 = Transaction(customer, coffee, 5)

        assert (coffee.calculate_total_number_of_transactions() == 2)

    def test_average_price(self):
        ''' Tests that the average price for a given coffee across all transactions can be calculated. '''
        coffee = Coffee("Espresso")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_2, coffee, 5)

        assert (coffee.calculate_average_price_across_all_transactions() == 3.5)