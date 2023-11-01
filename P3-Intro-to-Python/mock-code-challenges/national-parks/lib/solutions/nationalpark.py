class NationalPark:
    def __init__(self, name):
        self.name = name
        self.current_trips = []
        self.current_visitors = []
        self.current_visitations = {}
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        NAME_IS_STR = isinstance(name, str)
        NAME_DOESNT_EXIST = not hasattr(self, "name")
        if NAME_IS_STR and NAME_DOESNT_EXIST:
            self._name = name
        else:
            raise Exception("`NationalPark.name` already exists and/or must be a string!")
        
    def access_current_trips(self, new_trip=None):
        from solutions.trip import Trip
        TRIP_EXISTS = new_trip is not None
        TRIP_TYPE_IS_VALID = isinstance(new_trip, Trip)
        if TRIP_EXISTS and TRIP_TYPE_IS_VALID:
            self.current_trips.append(new_trip)
        return self.current_trips
    
    def access_current_visitors(self, new_visitor=None):
        from solutions.visitor import Visitor
        VISITOR_EXISTS = new_visitor is not None
        VISITOR_IS_UNIQUE = new_visitor not in self.current_visitors
        VISITOR_TYPE_IS_VALID = isinstance(new_visitor, Visitor)
        if VISITOR_EXISTS and VISITOR_TYPE_IS_VALID and VISITOR_IS_UNIQUE:
            self.current_visitors.append(new_visitor)   
        return self.current_visitors
    
    def calculate_all_trips(self):
        return len(self.current_trips)
    
    def check_most_frequent_visitor(self):
        return max(self.current_visitations, key=self.current_visitations.get)
            