

class Location:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def repr(self):
        return f"Latitude: {self.lat}, Longitude: {self.lon}"

    def str(self):
        return f"Latitude: {self.lat}, Longitude: {self.lon}"