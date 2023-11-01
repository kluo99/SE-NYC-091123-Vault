import pytest

from classes.nationalpark import NationalPark
from classes.visitor import Visitor
from classes.trip import Trip

class TestTrip:
    ''' Testing class for assessing stability of `trip.Trip` object. '''

    def test_has_a_visitor(self):
        ''' Tests that a trip has a visitor.'''
        visitor1 = Visitor("Bartholomew")
        visitor2 = Visitor("Archibald")
        park = NationalPark("Flatiron School")
        trip1 = Trip(visitor1, park)
        trip2 = Trip(visitor2, park)

        assert (trip1.visitor == visitor1)
        assert (trip2.visitor == visitor2)

    def test_visitor_of_type_visitor(self):
        ''' Tests that a trip's visitor is of type `Visitor`. '''
        park = NationalPark("Grand Canyon")
        visitor = Visitor("Andrew")
        trip = Trip(visitor, park)

        assert (isinstance(trip.visitor, Visitor))

    def test_has_a_park(self):
        ''' Tests that a trip has a visitor.'''
        visitor = Visitor("Bartholomew")
        park1 = NationalPark("Flatiron School")
        park2 = NationalPark("Roundwrinkle Resort")
        trip1 = Trip(visitor, park1)
        trip2 = Trip(visitor, park2)

        assert (trip1.national_park == park1)
        assert (trip2.national_park == park2)

    def test_park_of_type_park(self):
        ''' Tests that a trip's visitor is of type `Visitor`. '''
        park = NationalPark("Grand Canyon")
        visitor = Visitor("Andrew")
        trip = Trip(visitor, park)

        assert (isinstance(trip.national_park, NationalPark))

    def test_get_all_trips(self):
        ''' Tests that the `Trip` class is tracking all current instances in a list attribute. '''
        Trip.catalog = []

        visitor = Visitor("Bartholomew")
        park1 = NationalPark("Flatiron School")
        park2 = NationalPark("Roundwrinkle Resort")
        trip1 = Trip(visitor, park1)
        trip2 = Trip(visitor, park2)

        assert (trip1 in Trip.catalog)
        assert (trip2 in Trip.catalog)

    def test_get_total_number_of_trips(self):
        ''' Tests that the `Trip` class is tracking a global counter of created instances. '''
        Trip.counter = 0

        visitor = Visitor("Bartholomew")
        park1 = NationalPark("Flatiron School")
        park2 = NationalPark("Roundwrinkle Resort")
        trip1 = Trip(visitor, park1)
        trip2 = Trip(visitor, park2)

        assert (Trip.counter == 2)