import pytest

from classes.coffee import Coffee
from classes.customer import Customer
from classes.transaction import Transaction

class TestCustomer:
    ''' Testing class for assessing stability of `customer.Customer` object. '''

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

    def test_has_many_transactions(self):
        ''' Tests that a customer can have many transactions. '''
        coffee = Coffee("Cappuccino")
        customer_1 = Customer('Steve')
        customer_2 = Customer('Dima')
        transaction_1 = Transaction(customer_1, coffee, 2)
        transaction_2 = Transaction(customer_1, coffee, 5)
        transaction_3 = Transaction(customer_2, coffee, 5)

        assert (len(customer_1.access_current_transactions()) == 2)
        assert (not transaction_3 in customer_1.access_current_transactions())
        assert (transaction_1 in customer_1.access_current_transactions())
        assert (transaction_2 in customer_1.access_current_transactions())

    def test_transactions_of_type_transaction(self):
        ''' Tests that a customer's transactions are each of type `Transaction`. '''
        coffee = Coffee("Cappuccino")
        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee, 2)
        transaction_2 = Transaction(customer, coffee, 5)

        assert (isinstance(customer.access_current_transactions()[0], Transaction))
        assert (isinstance(customer.access_current_transactions()[1], Transaction))

    def test_has_many_coffees(self):
        ''' Tests that a customer can have many coffees. '''
        coffee_1 = Coffee("Cappuccino")
        coffee_2 = Coffee("Macchiatto")

        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee_1, 2)
        transaction_2 = Transaction(customer, coffee_2, 5)

        assert (coffee_1 in customer.access_current_coffees())
        assert (coffee_2 in customer.access_current_coffees())

    def test_has_unique_coffees(self):
        ''' Tests that a customer has a unique list of all the coffees that they have ordered. '''
        coffee_1 = Coffee("Cappuccino")
        coffee_2 = Coffee("Macchiatto")

        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee_1, 2)
        transaction_2 = Transaction(customer, coffee_1, 2)
        transaction_3 = Transaction(customer, coffee_2, 5)

        assert (len(set(customer.access_current_coffees())) == len(customer.access_current_coffees()))
        assert (len(customer.access_current_coffees()) == 2)

    def test_can_place_order(self):
        ''' Tests that a customer can place an order/transaction using a string name and numerical price. '''
        coffee = Coffee("Espresso")
        customer = Customer('Steve')
        transaction = customer.place_order("Espresso", 3)
        assert (coffee in customer.access_current_coffees())
        assert (transaction.price == 3)

    def test_get_total_money(self):
        ''' Tests that a customer can add up prices across all transactions. '''
        coffee_1 = Coffee("Cappuccino")
        coffee_2 = Coffee("Macchiatto")

        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee_1, 2)
        transaction_2 = Transaction(customer, coffee_1, 2)
        transaction_3 = Transaction(customer, coffee_2, 5)
        assert (customer.calculate_total_money_spent() == 9)

    def test_get_coffees_in_range(self):
        ''' Tests that a customer can get all coffees that fall within provided price range. '''
        coffee_1 = Coffee("Cappuccino")
        coffee_2 = Coffee("Caramel Macchiatto")
        coffee_3 = Coffee("Premium Ultra Dubai Espresso")

        customer = Customer('Steve')
        transaction_1 = Transaction(customer, coffee_1, 3)
        transaction_2 = Transaction(customer, coffee_2, 6)
        transaction_3 = Transaction(customer, coffee_3, 25)

        assert (coffee_1 in customer.retrieve_coffees_within_price_range(1, 10))
        assert (coffee_2 in customer.retrieve_coffees_within_price_range(1, 10))
        assert (coffee_3 not in customer.retrieve_coffees_within_price_range(1, 10))