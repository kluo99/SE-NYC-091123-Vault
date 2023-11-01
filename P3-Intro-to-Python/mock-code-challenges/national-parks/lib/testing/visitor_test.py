import pytest

from classes.nationalpark import NationalPark
from classes.visitor import Visitor
from classes.trip import Trip

class TestVisitor:
    ''' Testing class for assessing stability of `visitor.Visitor` object. '''

    def test_has_name(self):
        '''Visitor is initialized with a name'''
        visitor = Visitor("John")
        assert (visitor.name == "John")

    def test_name_is_string(self):
        '''Visitor is initialized with a name of type str'''
        visitor = Visitor("Bob")
        assert (isinstance(visitor.name, str))
        
        with pytest.raises(Exception):
            Visitor(2)

    def test_name_setter(self):
        '''Cannot change the name of the visitor'''
        vis = Visitor("Poppy")
        with pytest.raises(Exception):
            vis.name = "Warren"

    def test_has_many_trips(self):
        '''Visitor has many Trips.'''
        p1 = NationalPark("Yosemmette")
        vis = Visitor("Bill")
        vis2 = Visitor('Steve')
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p1)
        t_3 = Trip(vis2, p1)

        assert (len(vis.access_current_trips()) == 2)
        assert (t_1 in vis.access_current_trips())
        assert (t_2 in vis.access_current_trips())
        assert (not t_3 in vis.access_current_trips())

    def test_trips_of_type_trips(self):
        '''Visitor trips are of type '''
        vis = Visitor("Phil")
        p1 = NationalPark('Yellow Stone')
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p1)

        assert (isinstance(vis.access_current_trips()[0], Trip))
        assert (isinstance(vis.access_current_trips()[1], Trip))

    def test_has_many_parks(self):
        '''Visitor has many parks.'''
        vis = Visitor("Flat White")

        p1 = NationalPark('Alaska Wilds')
        p2 = NationalPark('Bryce Canyon')
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p2)

        assert (vis in p1.access_current_visitors())
        assert (vis in p2.access_current_visitors())

    def test_has_unique_parks(self):
        '''Visitor has unique list of all the parks they have visited.'''

        p1 = NationalPark("Yosemmette")
        p2 = NationalPark("Rocky Mountain")
        vis = Visitor('Steeve')
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p1)
        t_3 = Trip(vis, p2)

        assert (len(set(vis.access_current_parks())) == len(vis.access_current_parks()))
        assert (len(vis.access_current_parks()) == 2)

    def test_customers_of_type_customer(self):
        '''Visitor nationalparks are of type NationalPark'''
        p1 = NationalPark("Yosemmette")
        p2 = NationalPark("Rocky Mountain")
        vis = Visitor('Steeeve')
        t_1 = Trip(vis, p1)
        t_3 = Trip(vis, p2)

        assert (isinstance(vis.access_current_parks()[0], NationalPark))
        assert (isinstance(vis.access_current_parks()[1], NationalPark))