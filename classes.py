from time import time
from collections import OrderedDict

class Station:
    '''
    Class used to represent an MTA train station
    ## Member Variables
        station_name -> name of the station
        north_bound_arriving_in -> used to keep track of the times
                                    for arriving north bound trains
        south_bound_arriving_in -> used to keep track of the times
                                    for arriving south bound trains
    '''
    def __init__(self, station_name):
        self.station_name = station_name
        self.north_bound_arriving_in = []
        self.south_bound_arriving_in = []

    def add_north(self, time):
        '''
        Add a time to the list of north bound arriving times
        '''
        self.north_bound_arriving_in.append(time)

    def add_south(self, time):
        '''
        Add a time to the list of north bound arriving times
        '''
        self.south_bound_arriving_in.append(time)

    def get_name(self):
        '''
        Return the name of this station
        '''
        return self.station_name

    def get_norths(self):
        '''
        Return the list of times for arriving north bound trains
        '''
        return sorted(self.north_bound_arriving_in)

    def get_souths(self):
        '''
        Return the list of times for arriving south bound trains
        '''
        return sorted(self.south_bound_arriving_in)

    def show(self):
        '''
        Print the station.
        '''
        to_print = ""
        to_print += self.station_name + "\n"
        to_print += "North Bound:\n"
        for time in sorted(self.north_bound_arriving_in):
            to_print += str(self.__time_diff(time)) + " "
        to_print += "\nSouth Bound:\n"
        for time in sorted(self.south_bound_arriving_in):
            to_print += str(self.__time_diff(time)) + " "
        print to_print

    def __time_diff(self, later_time):
        '''
        Utility function used in this class to return 
        the difference between two times 
        '''
        now = time()
        return int(later_time - now)/60

class Stations:
    '''
    Container class used to hold an dictionary of Stations
    ## Member Variables
        stations -> a dictionary of station name/Station pairs
    '''
    def __init__(self):
        self.stations = OrderedDict()

    def show(self):
        '''
        Print all the stations held by this class
        '''
        for station in self.stations:
            self.stations[station].show()
            print

    def __getitem__(self, key):
        '''
        Definition of how operator [] behaves for this class
        '''
        if key in self.stations:
            return self.stations[str(key)]
        else:
            station = Station(key)
            self.stations[str(key)] = station
            return self.stations[key]