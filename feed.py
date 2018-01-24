from utils import parseArguments
from utils import populate_stations
from utils import get_entities_for

if __name__ == "__main__":
    train_line = parseArguments()
    stations = populate_stations(get_entities_for(train_line))
    stations.show()