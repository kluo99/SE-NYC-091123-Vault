# Mock Code Challenge - Coffeeshop (Object Relationships)

For this assignment, we'll be working with a coffeeshop-style domain.

We have three models: `Coffee`, `Customer`, and `Transaction`.

For our purposes, a `Coffee` has many `Transaction`s, a `Customer` has many
`Transaction`s, and a `Transaction` belongs to a `Customer` and to a `Coffee`.

`Coffee` - `Customer` is a many-to-many relationship. 

**Note**: You should draw your domain on paper or on a whiteboard _before you
start coding_. Remember to identify a single source of truth for your data.

## Topics

- Classes and Instances
- Class and Instance Methods
- Variable Scope
- Object Relationships
- lists and list Methods

## Instructions

**To Get Started!** 

Run `pipenv install` while inside of this directory.

**Starting Out!** 

Build out all of the methods listed in the deliverables. The methods are listed
in a suggested order, but you can feel free to tackle the ones you think are
easiest. Be careful: some of the later methods rely on earlier ones.

**Testing Your Code!** 

This code challenge has tests to help you check your work. You
can run `pytest` to make sure your code is functional before submitting.

**Before you submit!** 

Save and run your code to verify that it works as you
expect. If you have any methods that are not working yet, feel free to leave
comments describing your progress.

## Guidelines

We've provided you with a tool that you can use to test your code. To use it,
run `python debug.py` from the command line. This will start a `ipdb` session
with your classes defined. You can test out the methods that you write here. You
can add code to the `debug.py` file to define variables and create sample
instances of your objects.

Writing error-free code is more important than completing all of the
deliverables listed - prioritize writing methods that work over writing more
methods that don't work. You should test your code in the console as you write.

Similarly, messy code that works is better than clean code that doesn't. First,
prioritize getting things working. Then, if there is time at the end, refactor
your code to adhere to best practices. When you encounter duplicated logic,
extract it into a shared helper method.

## Deliverables

Write the following methods in the classes in the files provided. Feel free to
build out any helper methods if needed.

### Initializers and Properties

#### Customer

- 
  ```python
  def __init__(self, name)
  ```
  - Customer should be initialized with a name 
- 
  ```python
  @property
  def name(self)
  ```
    - Returns the customer's name, as a string
- 
  ```python
  @name.setter
  def name(self, name)
  ```
    - Names must be of type `str`
    - Names must be at least 1 character and at most 15 characters long
    - `raise Exception` if setter fails
      

#### Coffee

- 
  ```python
  def __init__(self, name)
  ```
  - Coffees should be initialized with a name, as a string
- 
  ```python
  @property
  def name(self)
  ```
    - Returns the coffee's name
- 
  ```python
  @name.setter
  def name(self, name)
  ```
    - Should not be able to change after the coffee is created
      - _hint: `hasattr()`_
    - `raise Exception` if setter fails

#### Transaction

- 
    ```python
    def __init__(self, customer, coffee, price)
    ```
  - Transactions should be initialized with a customer, coffee, and a price (a number)
- 
  ```python
  @property
  def price(self)
  ```
    - Returns the price for an transaction
- 
  ```python
  @price.setter
  def price(self, price)
  ```
    - Price must be at least 1 and no greater than 50
    - `raise Exception` if setter fails
- 
  ```python
  @property
  def customer(self)
  ```
    - Returns the customer object for that transaction
- 
  ```python
  @customer.setter
  def customer(self, customer)
  ```
    - The argument `customer` must be of type `Customer`
    - `raise Exception` if setter fails
- 
  ```python
  @property
  def coffee(self)
  ```
    - Returns the coffee object for that transaction
- 
  ```python
  @coffee.setter
  def coffee(self, coffee)
  ```
    - The argument `coffee` must be of type `Coffee` 
    - `raise Exception` if setter fails

### Object Relationship Methods


#### Coffee

- 
  ```python
  def access_current_transactions(new_transaction=None)
  ```
  - Adds `new_transaction` to `Coffee`'s transactions
  - Returns a list of all transactions for that coffee
  - Transactions must be of type `Transaction`
  - _Will be called from `Transaction.__init__`_
- 
  ```python
  def access_current_customers(new_customer=None)
  ```
  - Adds new customers to coffee
  - Returns a list of all **unique** customers who have ordered a particular coffee (i.e. the list will not contain the same customer more than once).
    - The list must only contain objects of type `Customer`
  - _Will be called from `Transaction.__init__`_

#### Customer

- 
  ```python
  def access_current_transactions(new_transaction=None)
  ```
  - Adds new transactions to customer
  - Returns a list of all transactions a customer has ordered
  - Transactions must be of type `Transaction`
  - _Will be called from `Transaction.__init__`_
- 
  ```python
  def access_current_coffees(new_coffee=None)
  ```
  - Adds new coffees to customer
  - Returns a list of all **unique** coffees a customer has ordered (i.e. the list will not contain the same coffee more than once).
    - The list must only contain objects of type `Coffee`
  - _Will be called from `Transaction.__init__`_

### Aggregate and Association Methods

#### Customer

-
  ```python
  def place_order(name_of_coffee, price)
  ```
  - Given the name of a coffee (as a string) and a price (as an integer), creates a new transaction and associates it with that customer and coffee
    - _hint: Remember to import both objects!_
  - Returns the new transaction as an object instance
- 
  ```python
  def calculate_total_money_spent()
  ```
  - Returns the total quantity of money spent across all transactions for that customer
- 
  ```python
  def retrieve_coffees_within_price_range(min_price=0, max_price=999)
  ```
  - Returns the coffees that fall within a defined price range
    - _hint: `filter()`_
  - Range specified by values provided by `min_price` and `max_price`
    - If `min_price` isn't specified, defaults to `0`
    - If `max_price` isn't specified, defaults to `999`
  - Filtered coffees (_get it?_) should be returned as a list

#### Coffee

- 
  ```python
  def calculate_total_number_of_transactions()
  ```
  - Returns the total number of times that coffee has been ordered
- 
  ```python
  def calculate_average_price_across_all_transactions()
  ```
  - Returns the average price for a coffee based on its transactions
  - Reminder: you can calculate the average by adding up all the transaction's prices and
    dividing by the total number of transactions
    - _hint:_ Might we have a method for quickly calculating the total number of transactions?