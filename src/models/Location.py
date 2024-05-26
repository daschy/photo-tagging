from models.Base import Base


class Location(Base):
  def __init__(self):
    self.city = None
    self.state = None
    self.country = None
    self.postal_code = None
    self.road = None
