class Location:
    def __init__(self):
        # self.address = None
        self.city = None
        self.state = None
        self.country = None
        self.postal_code = None
        self.road=None
    def __str__(self):
        attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return ', '.join(attributes)