# Mock Code Challenge - National Parks (Object Relationships)

For this assignment, we'll be working with a national park planner-style domain.

We have three models: `NationalPark`, `Visitor`, and `Trip`.

For our purposes, a `NationalPark` has many `Trip`s, a `Visitor` has many
`Trip`s, and a `Trip` belongs to a `Visitor` and to a `NationalPark`.

`NationalPark` - `Visitor` is a many to many relationship.

**Note**: You should draw your domain on paper or on a whiteboard _before you
start coding_. Remember to identify a single source of truth for your data.

## Topics

- Classes and Instances
- Class and Instance Methods
- Variable Scope
- Object Relationships
- lists and list Methods

## Instructions

To get started, run `pipenv install` while inside of this directory.

Build out all of the methods listed in the deliverables. The methods are listed
in a suggested order, but you can feel free to tackle the ones you think are
easiest. Be careful: some of the later methods rely on earlier ones.

**Remember!** This code challenge has tests to help you check your work. You
can run `pytest` to make sure your code is functional before submitting.

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

**Before you submit!** Save and run your code to verify that it works as you
expect. If you have any methods that are not working yet, feel free to leave
comments describing your progress.

## Deliverables

Write the following methods in the classes in the files provided. Feel free to
build out any helper methods if needed.

### Initializers and Properties

#### Visitor

- 
  ```python
  def __init__(self, name)
  ```
  - Should be initialized with a name.
- 
  ```python
  @property
  def name(self)
  ```
  - Returns the visitor's name, as a string.
- 
  ```python
  @name.setter
  def name(self, name)
  ```
  - A name must be a `str`.
  - A name must be at least 1 character and at most 15 characters long.
  - Once the visitor is instantiated with a name, their name should not change.
    - _HINT: `hasattr()` can help!_
  - If these validations are violated, a custom exception should be raised.

#### NationalPark

- 
  ```python
  def __init__(self, name)
  ```
  - Should be initialized with a name.
- 
  ```python
  @property
  def name(self)
  ```
  - Returns the national park's name, as a string.
- 
  ```python
  @name.setter
  def name(self, name)
  ```
  - A name must be a `str`.
  - Once the national park is instantiated with a name, its name should not change.
    - _HINT: `hasattr()` can help!_
  - If these validations are violated, a custom exception should be raised.

#### Trip

- 
    ```python
    def __init__(self, visitor, national_park, start_date=None, end_date=None)
    ```
    - Transactions should be initialized with a visitor, a national park, a start date, and an end date.
      - _Functioning start date and end date logic have been provided for you._
- 
  ```python
  @property
  def visitor(self)
  ```
    - Returns the visitor object for that trip
- 
  ```python
  @visitor.setter
  def visitor(self, visitor)
  ```
    - The argument `visitor` must be of type `Visitor`
    - `raise Exception` if setter fails
- 
  ```python
  @property
  def national_park(self)
  ```
    - Returns the national park object for that transaction
- 
  ```python
  @national_park.setter
  def national_park(self, national_park)
  ```
    - The argument `national_park` must be of type `NationalPark` 
    - `raise Exception` if setter fails

### Object Relationship Methods and Properties

#### Visitor

- 
  ```python
  def access_current_trips(new_trip=None)
  ```
  - Potentially adds a `new_trip` to `Visitor`'s trips
  - Returns a list of all trips for that visitor
  - Trips must be of type `Trip`
  - _Will be called from `Trip.__init__`_
- 
  ```python
  def access_current_parks(new_park=None)
  ```
  - Potentially adds a `new_park` to `Visitor`'s parks
  - Returns a list of all **unique** national parks that the current visitor has visited (i.e. the list will not contain the same national park more than once).
    - The list must only contain objects of type `NationalPark`
  - _Will be called from `Trip.__init__`_ 

#### NationalPark

- 
  ```python
  def access_current_trips(new_trip=None)
  ```
  - Potentially adds a `new_trip` to `Visitor`'s trips
  - Returns a list of all trips for that visitor
  - Trips must be of type `Trip`
  - _Will be called from `Trip.__init__`_
- 
  ```python
  def access_current_visitors(new_visitor=None)
  ```
  - Potentially adds a `new_visitor` to `NationalPark`'s visitors
  - Returns a list of all **unique** visitors that the current park has received (i.e. the list will not contain the same visitor more than once).
    - The list must only contain objects of type `Visitor`
  - _Will be called from `Trip.__init__`_ 

### Aggregate and Association Methods

#### National Park

- 
  ```python
  def calculate_all_trips()
  ```
  - Returns the total number of times that the current park has been visited
- 
  ```python
  def check_most_frequent_visitor()
  ```
  - Returns the visitor who has visited the current park the most number of times
    - _HINT: The built-in function `max()` can help!_

### Stretch Challenges

- **Extend all three objects with property deleters.**

- **Write additional property getters and setters within `Trip` for validating the `start_date` and `end_date`.**
  - _HINT: You may want to research how `datetime` objects work!_
  
- **Create a third aggregate/association method called `NationalPark.rank_parks()` which sorts all national parks in ascending order based on number of visitations.**