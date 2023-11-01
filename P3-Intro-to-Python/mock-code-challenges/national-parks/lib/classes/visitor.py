class Visitor:    
    def __init__(self, name):
        self.name = name
        
    def access_current_trips(self, new_trip=None):
        from classes.trip import Trip
        pass
    
    def access_current_parks(self, new_park=None):
        from classes.nationalpark import NationalPark
        pass