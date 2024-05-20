from Models.Base import Base


class Caption(Base):
  def __init__(self, text: str, model_name: str):
    self.text = text
    self.model_name = model_name
