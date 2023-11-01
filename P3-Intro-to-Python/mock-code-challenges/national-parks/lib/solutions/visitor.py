class Visitor:    
    def __init__(self, name):
        self.name = name
        self.current_trips = []
        self.current_parks = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        NAME_IS_STR = isinstance(name, str)
        NAME_DOESNT_EXIST = not hasattr(self, "name")
        NAME_IN_ACCEPTABLE_LENGTH = (1 <= len(name) <= 15)
        if NAME_IS_STR and NAME_DOESNT_EXIST and NAME_IN_ACCEPTABLE_LENGTH:
            self._name = name
        else:
            raise Exception("`Visitor.name` must be a string inclusively between one (1) and fifteen (15) characters!")
        
    def access_current_trips(self, new_trip=None):
        from solutions.trip import Trip
        TRIP_EXISTS = new_trip is not None
        TRIP_TYPE_IS_VALID = isinstance(new_trip, Trip)
        if TRIP_EXISTS and TRIP_TYPE_IS_VALID:
            self.current_trips.append(new_trip)
        return self.current_trips
    
    def access_current_parks(self, new_park=None):
        from solutions.nationalpark import NationalPark
        PARK_EXISTS = new_park is not None
        PARK_IS_UNIQUE = new_park not in self.current_parks
        PARK_TYPE_IS_VALID = isinstance(new_park, NationalPark)
        if PARK_EXISTS and PARK_IS_UNIQUE and PARK_TYPE_IS_VALID:
            self.current_parks.append(new_park)
        return self.current_parks