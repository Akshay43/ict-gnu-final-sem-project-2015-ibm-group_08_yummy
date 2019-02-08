class Timing:
    """TODO: Add all timing operation from datetime module"""
    def __init__(self, open, close):
        self.open = open
        self.close = close


    def __str__(self):
        """ TODO: update str"""
        return self.__dict__
