import csv
import urllib2
from google.transit import gtfs_realtime_pb2
import requests
import time



def getStations():
    '''
    Return a list of all stations in the system
    eg:
    ['1', '1', 'R01', 'BMT', 'Astoria', 'Astoria - Ditmars Blvd', 'Q', 'N W', 'Elevated', '40.775036', '-73.912034']
    ['2', '2', 'R03', 'BMT', 'Astoria', 'Astoria Blvd', 'Q', 'N W', 'Elevated', '40.770258', '-73.917843']
    ...
    '''
    stations_csv_url = "http://web.mta.info/developers/data/nyct/subway/Stations.csv"
    response = urllib2.urlopen(stations_csv_url)
    return list(csv.reader(response))

def getEntitiesFor(train_line):

    # Key = train line
    # Value = url id
    lines = {'1' : 1,
             '2' : 1,
             '3' : 1,
             '4' : 1,
             '5' : 1,
             'S' : 1,
             'A' : 26,
             'C' : 26,
             'E' : 26,
             'N' : 16,
             'Q' : 16,
             'R' : 16,
             'W' : 16,
             'B' : 21,
             'D' : 21,
             'F' : 21,
             'M' : 21,
             'L' : 2,
             'SIR' : 11,
             'G' : 31,
             'J' : 36,
             'Z' : 36}

    # Check to make sure feed data is available for that line
    if train_line not in lines:
        print "Invalid line!"
        return

    key = #<ENTER_KEY_HERE> 
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://datamine.mta.info/mta_esi.php?key={}&feed_id={}'.format(key, 
                                                                                            lines[train_line]))
    feed.ParseFromString(response.content)

    entities = []
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            if entity.trip_update.trip.route_id == train_line:
                entities.append(entity)
    
    return entities

def printEntities(entities):
    stations = getStations()

    for entity in entities:
        print entity.id

        stop_time_update = entity.trip_update.stop_time_update
        for stu in stop_time_update:
            stop         = str(stu.stop_id).strip()
            arrival_time = str(stu.arrival).strip()[6:]

            for station in stations:
                if station[2] == stop[:-1]:
                    print stop[len(stop)-1], station[5], timeDiff(arrival_time), "min"

        print

def timeDiff(arrival_time):
    now = time.time()
    return (int(arrival_time)-int(now))/60



class Station:
    north_bound_arriving_in = []
    south_bound_arriving_in = []
    station_name = ""

    def __init__(self, name):
        self.station_name = name

    def add_north(self, time):
        self.north_bound_arriving_in.append(time)

    def add_south(self, time):
        self.south_bound_arriving_in.append(time)

    def name(self):
        return self.station_name

    def north(self):
        return sorted(self.north_bound_arriving_in)

    def south(self):
        return sorted(self.south_bound_arriving_in)

class Stations:
    stations = {}

    def add(self,station):
        self.stations[station.name()] = station

    def exists(self,station_name):
        if station_name in self.stations:
            return True
        else: 
            return False



#printEntities(getEntitiesFor("Q"))

station = Station("82")

stations = Stations()
print stations.exists("82")
stations.add(station)
print stations.exists("82")