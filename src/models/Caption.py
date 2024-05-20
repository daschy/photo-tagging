from src.Models.Base import Base


class Caption(Base):
    def __init__(self, text: str, modelName: str):
        self.text = text
        self.modelName = modelName
