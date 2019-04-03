from dataclasses import dataclass
from google.cloud.firestore_v1beta1._helpers import GeoPoint
from .address import Address
from .timing import Timing


@dataclass
class RestaurantBranch:
    address: Address
    location: GeoPoint
    no_of_tables: int
    table_max_capacity: int
    timing: Timing
