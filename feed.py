from utils import populate_stations
from utils import get_entities_for

if __name__ == "__main__":
    stations = populate_stations(get_entities_for("1"))
    stations.show()
