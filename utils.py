from csv import reader
from google.transit import gtfs_realtime_pb2
from time import time
from requests import get
from urllib2 import urlopen

from classes import Station
from classes import Stations


mta_api_key = #INSERT API KEY HERE

def get_stations():
    '''
    Return a list of all stations in the system
    eg:
    ['1', '1', 'R01', 'BMT', 'Astoria', 'Astoria - Ditmars Blvd', 'Q', 'N W', 'Elevated', '40.775036', '-73.912034']
    ['2', '2', 'R03', 'BMT', 'Astoria', 'Astoria Blvd', 'Q', 'N W', 'Elevated', '40.770258', '-73.917843']
    ...
    '''
    stations_csv_url = "http://web.mta.info/developers/data/nyct/subway/Stations.csv"
    response = urlopen(stations_csv_url)
    return list(reader(response))

def get_station_name(stop_id, station_names):
    '''
    Using all station names return the actual station name 
    for the given stop_id. If the actual station name does
    not exist then use the stop_id as the station name
    '''
    station_name = stop_id
    for station in station_names:
        if station[2] == stop_id:
            station_name = station

    if station_name == stop_id:
        return stop_id

    return station_name[5]

def get_entities_for(train_line):
    '''
    Make an MTA API call to retrieve all the entities 
    for the given train tile. 

    NOTE: When providing a train line the API might 
    return multiple train lines. This function
    extracts only the train line requested in the train_line
    argument
    '''

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

    key = mta_api_key
    feed = gtfs_realtime_pb2.FeedMessage()
    response = get('http://datamine.mta.info/mta_esi.php?key={}&feed_id={}'.format(key, 
                                                                                            lines[train_line]))
    feed.ParseFromString(response.content)

    entities = []
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            if entity.trip_update.trip.route_id == train_line:
                entities.append(entity)
    
    return entities

def populate_stations(entities):
    '''
    Using the entities argument this function creates 
    stations and populates them with their train arrival
    times
    '''

    station_names = get_stations()
    stations = Stations()

    for entity in entities:
        stop_time_updates = entity.trip_update.stop_time_update

        for stop_time_update in stop_time_updates:

            stop_id = str(stop_time_update.stop_id).strip()[:-1]
            station_name = str(get_station_name(stop_id,station_names))
            train_direction = str(stop_time_update.stop_id).strip()[-1:]
            arrival_time = str(stop_time_update.arrival).strip()[6:]

            if train_direction == "N":
                stations[station_name].add_north(int(arrival_time))
            elif train_direction == "S":
                stations[station_name].add_south(int(arrival_time))
            else:
                # Should never happen since train 
                # is either "N" bound or "S" bound
                assert False

    return stations