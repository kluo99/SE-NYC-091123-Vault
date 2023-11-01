class Trip:
    counter, catalog = 0, []
    def __init__(self, visitor, national_park, start_date=None, end_date=None):
        self.visitor = visitor
        self.national_park = national_park

        Trip.counter += 1
        Trip.catalog.append(self)

        # DO NOT EDIT – Datetime Initialization Script –––––––––––– #
        NO_START_DATE_PROVIDED = (start_date is None)               #
        NO_END_DATE_PROVIDED = (end_date is None)                   #
        if NO_START_DATE_PROVIDED or NO_END_DATE_PROVIDED:          #
            from datetime import date, timedelta                    #
            if NO_START_DATE_PROVIDED:                              #
                self.start_date = date.today()                      #
            if NO_END_DATE_PROVIDED:                                #
                self.end_date = date.today() + timedelta(days=1)    #
        else:                                                       #
            self.start_date, self.end_date = start_date, end_date   #
        # DO NOT EDIT – Datetime Initialization Script –––––––––––– #

        visitor.access_current_trips(self)
        visitor.access_current_parks(national_park)

        national_park.access_current_trips(self)
        national_park.access_current_visitors(visitor)

        if visitor in national_park.current_visitations:
            national_park.current_visitations[visitor] += 1
        else:
            national_park.current_visitations[visitor] = 1

    def __repr__(self):
        from datetime import datetime
        return f"{self.visitor.name} is going on a trip to {self.national_park.name} from {datetime.strftime(self.start_date, '%m/%d/%Y')} to {datetime.strftime(self.end_date, '%m/%d/%Y')}."

    @property
    def visitor(self):
        return self._visitor
    
    @visitor.setter
    def visitor(self, visitor):
        from solutions.visitor import Visitor
        VISITOR_TYPE_IS_VALID = isinstance(visitor, Visitor)
        if VISITOR_TYPE_IS_VALID:
            self._visitor = visitor
        else:
            raise Exception("Unacceptable data type for `Trip.visitor`!")
        
    @property
    def national_park(self):
        return self._national_park
    
    @national_park.setter
    def national_park(self, national_park):
        from solutions.nationalpark import NationalPark
        PARK_TYPE_IS_VALID = isinstance(national_park, NationalPark)
        if PARK_TYPE_IS_VALID:
            self._national_park = national_park
        else:
            raise Exception("Unacceptable data type for `Trip.national_park`!")