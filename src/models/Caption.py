class Caption:
    def __init__(self, text: str, modelName: str):
        self.text = text
        self.modelName = modelName

    def __str__(self):
        attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return ", ".join(attributes)

    def __repr__(self):
        return self.__str__()