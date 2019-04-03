from dataclasses import dataclass


@dataclass
class Address:
    area: str
    city: str
    country: str
    landmark: str
    near_locality: str
