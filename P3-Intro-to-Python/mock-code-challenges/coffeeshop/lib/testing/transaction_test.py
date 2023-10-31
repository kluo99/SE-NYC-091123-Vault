import pytest

from classes.coffee import Coffee
from classes.customer import Customer
from classes.transaction import Transaction

class TestTransactions:
    ''' Testing class for assessing stability of `transaction.Transaction` object. '''

    def test_has_price(self):
        ''' Tests that an transaction is initialized with a numerical price. '''
        coffee = Coffee("Cappuccino")
        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee, 2)
        transaction_2 = Transaction(customer, coffee, 5)

        assert (transaction_1.price == 2)
        assert (transaction_2.price == 5)

    def test_has_a_customer(self):
        ''' Tests that an transaction has a customer.'''
        coffee = Coffee("Cappuccino")
        customer_1 = Customer('Wayne')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_2, coffee, 5)

        assert (transaction_1.customer == customer_1)
        assert (transaction_2.customer == customer_2)

    def test_customer_of_type_customer(self):
        ''' Tests that a transaction's customer is of type `Customer`. '''
        coffee = Coffee("Espresso")
        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee, 2)
        transaction_2 = Transaction(customer, coffee, 5)

        assert (isinstance(transaction_1.customer, Customer))
        assert (isinstance(transaction_2.customer, Customer))

    def test_has_a_coffee(self):
        ''' Tests that a transaction has a coffee. '''
        coffee_1 = Coffee("Cappuccino")
        coffee_2 = Coffee("Espresso")
        customer = Customer('Wayne')
        transaction_1 = Transaction(customer, coffee_1, 2)
        transaction_2 = Transaction(customer, coffee_2, 5)

        assert (transaction_1.coffee == coffee_1)
        assert (transaction_2.coffee == coffee_2)

    def test_coffee_of_type_coffee(self):
        ''' Tests that an transaction's coffee is of type `Coffee`. '''
        coffee = Coffee("Espresso")
        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee, 2)
        transaction_2 = Transaction(customer, coffee, 5)

        assert (isinstance(transaction_1.coffee, Coffee))
        assert (isinstance(transaction_2.coffee, Coffee))

    def test_get_all_transactions(self):
        ''' Tests that the `Transaction` class is tracking all current instances in a list attribute. '''
        Transaction.catalog = []
        coffee = Coffee("Cappuccino")
        customer_1 = Customer('Wayne')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_2, coffee, 5)

        assert (transaction_1 in Transaction.catalog)
        assert (transaction_2 in Transaction.catalog)

    def test_get_total_num_of_transactions(self):
        ''' Tests that the `Transaction` class is tracking a global counter of created instances. '''
        Transaction.counter = 0
        coffee = Coffee("Cappuccino")
        customer_1 = Customer('Wayne')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_2, coffee, 5)

        assert (Transaction.counter == 2)