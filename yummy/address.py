class Address:
    def __init__(self, area, city, country, landmark, near_locality):
        self.area = area
        self.city = city
        self.country = country
        self.landmark = landmark
        self.near_locality = near_locality

    def repr(self):
        return f"landmark: {self.landmark}, area: {self.area}, city: {self.city}," \
            f"country: {self.country}"

    def str(self):
        return self.__dict__

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, address):
        return cls(**address)
