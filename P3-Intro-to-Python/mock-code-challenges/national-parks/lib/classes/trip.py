class Trip:
    counter, catalog = 0, []
    def __init__(self, visitor, national_park, start_date=None, end_date=None):
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
        
        self.visitor = visitor
        self.national_park = national_park

        Trip.counter += 1
        Trip.catalog.append(self)

    def __repr__(self):
        from datetime import datetime
        return f"{self.visitor.name} is going on a trip to {self.national_park.name} from {datetime.strftime(self.start_date, '%m/%d/%Y')} to {datetime.strftime(self.end_date, '%m/%d/%Y')}."