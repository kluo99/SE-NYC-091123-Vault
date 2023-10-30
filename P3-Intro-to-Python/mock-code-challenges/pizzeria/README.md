# Mock Code Challenge - Python Pizzeria (Object Relationships)

For this assignment, we'll be working with a Pizza restaurant-style domain.

We have three models: `Pizza`, `Customer`, and `Order`.

For our purposes, a `Pizza` has many `Order`s, a `Customer` has many
`Order`s, and a `Order` belongs to a `Customer` and to a `Pizza`.

`Pizza` - `Customer` is a many-to-many relationship. 

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
      

#### Pizza

- 
  ```python
  def __init__(self, name)
  ```
  - Pizzas should be initialized with a name, as a string
- 
  ```python
  @property
  def name(self)
  ```
    - Returns the pizza's name
- 
  ```python
  @name.setter
  def name(self, name)
  ```
    - Should not be able to change after the pizza is created
      - _hint: `hasattr()`_
    - `raise Exception` if setter fails

#### Order

- 
    ```python
    def __init__(self, customer, pizza, price)
    ```
  - Orders should be initialized with a customer, pizza, and a price (a number)
- 
  ```python
  @property
  def price(self)
  ```
    - Returns the price for an order
- 
  ```python
  @price.setter
  def price(self, price)
  ```
    - Price must be at least 1 and no greater than 10
    - `raise Exception` if setter fails
- 
  ```python
  @property
  def customer(self)
  ```
    - Returns the customer object for that order
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
  def pizza(self)
  ```
    - Returns the pizza object for that order
- 
  ```python
  @coffee.setter
  def pizza(self, pizza)
  ```
    - The argument `pizza` must be of type `Pizza` 
    - `raise Exception` if setter fails

### Object Relationship Methods


#### Pizza

- 
  ```python
  def access_current_orders(new_order=None)
  ```
  - Adds `new_order` to `Pizza`'s orders
  - Returns a list of all orders for that pizza
  - orders must be of type `Order`
  - _Will be called from `Order.__init__`_
- 
  ```python
  def access_current_customers(new_customer=None)
  ```
  - Adds new customers to pizza
  - Returns a list of all **unique** customers who have ordered a particular pizza (i.e. the list will not contain the same customer more than once).
    - The list must only contain objects of type `Customer`
  - _Will be called from `Order.__init__`_

#### Customer

- 
  ```python
  def access_current_orders(new_order=None)
  ```
  - Adds new orders to customer
  - Returns a list of all orders a customer has ordered
  - orders must be of type `Order`
  - _Will be called from `Order.__init__`_
- 
  ```python
  def access_current_pizzas(new_pizza=None)
  ```
  - Adds new pizzas to customer
  - Returns a list of all **unique** pizzas a customer has ordered (i.e. the list will not contain the same pizza more than once).
    - The list must only contain objects of type `Pizza`
  - _Will be called from `Order.__init__`_

### Aggregate and Association Methods


#### Pizza

- 
  ```python
  def calculate_total_number_of_orders()
  ```
  - Returns the total number of times that pizza has been ordered
- 
  ```python
  def calculate_average_price_across_all_orders()
  ```
  - Returns the average price for a pizza based on its orders
  - Reminder: you can calculate the average by adding up all the order's prices and
    dividing by the total number of orders
    - _hint:_ Might we have a method for quickly calculating the total number of orders?