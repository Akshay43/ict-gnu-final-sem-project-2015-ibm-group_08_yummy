from dataclasses import dataclass


@dataclass
class RestaurantBranch:
    pass


@dataclass
class RestaurantCollection:
    """Collections of Restaurants"""
    pass


@dataclass
class Restaurant:
    name: str
    rating: float
    branch: RestaurantBranch
    pass
