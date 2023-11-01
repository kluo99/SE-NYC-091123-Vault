import pytest

from classes.nationalpark import NationalPark
from classes.visitor import Visitor
from classes.trip import Trip

class TestNationalParks:
    ''' Testing class for assessing stability of `nationalpark.NationalPark` object. '''

    def test_has_name(self):
        '''NationalPark is initialized with a name'''
        np = NationalPark("Flatirons")
        assert (np.name == "Flatirons")

    def test_name_is_string(self):
        '''NationalPark is initialized with a name of type str'''
        np = NationalPark("Wild West")
        assert (isinstance(np.name, str))

        with pytest.raises(Exception):
            NationalPark(2)
     
    def test_name_setter(self):
        '''Cannot change the name of the NationalPark'''
        np = NationalPark("under the sea")
        
        with pytest.raises(Exception):
            np.name = "over the sea"

    def test_has_many__trips(self):
        '''NationalPark has many Trips.'''
        p1 = NationalPark("Yosemmette")
        p2 = NationalPark("Rocky Mountain")
        vis = Visitor('Steve')
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p1)
        t_3 = Trip(vis, p2)

        assert (len(p1.access_current_trips()) == 2)
        assert (t_1 in p1.access_current_trips())
        assert (t_2 in p1.access_current_trips())
        assert (not t_3 in p1.access_current_trips())

    def test_trips_of_type_trips(self):
        '''National Park trips are of type '''
        vis = Visitor("Phil")
        p1 = NationalPark('Yellow Stone')
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p1)

        assert (isinstance(p1.access_current_trips()[0], Trip))
        assert (isinstance(p1.access_current_trips()[1], Trip))

    def test_has_many_visitors(self):
        '''National Parks has many visitors.'''
        vis = Visitor("Tammothy")
        vis2 = Visitor('Bryce')

        p1 = NationalPark('Alaska Wilds')
        
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis2, p1)

        assert (vis in p1.access_current_visitors())
        assert (vis2 in p1.access_current_visitors())

    def test_has_unique_visitors(self):
        '''NationalParks has unique list of all the visitors that have visited.'''

        p1 = NationalPark("Yosemmette")
        vis = Visitor('Steeve')
        vis2 = Visitor('Wolfe')

        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p1)
        t_3 = Trip(vis2, p1)

        assert (len(set(p1.access_current_visitors())) == len(p1.access_current_visitors()))
        assert (len(p1.access_current_visitors()) == 2)

    def test_total_visits(self):
        '''Correct total visits'''
        p1 = NationalPark("Yosemmette")
        vis = Visitor('Sheryl')
        t_1 = Trip(vis, p1)
        t_2 = Trip(vis, p1)
        t_3 = Trip(vis, p1)
        assert p1.calculate_all_trips() == 3
    
    def test_best_visitor(self):
        '''Get the visitor that visited the park the most'''
        p1 = NationalPark("Yosemmette")
        vis = Visitor('Tom')
        vis2 = Visitor('Mark')
        t_1 = Trip(vis, p1)
        t_3 = Trip(vis, p1)
        t_3 = Trip(vis2, p1)
        assert(p1.check_most_frequent_visitor().name == "Tom")