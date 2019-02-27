from dataclasses import dataclass
from .restaurant_branch import RestaurantBranch


@dataclass
class Restaurant:
    name: str
    rating: float
    branch: RestaurantBranch
    pass
