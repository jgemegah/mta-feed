from utils import populate_stations
from utils import get_entities_for
from sys import dont_write_bytecode

#Prevent python from creating .pyc files
dont_write_bytecode = True 

if __name__ == "__main__":
    stations = populate_stations(get_entities_for("G"))
    stations.show()
