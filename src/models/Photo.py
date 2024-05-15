from typing import List

class Photo:
    def __init__(self, path, fingerprint, keywords: List[str] | None):
        self.path = path
        self.keywords: List[str] = keywords | []
        self.fingerprint = fingerprint

    def __str__(self):
        attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return ", ".join(attributes)

    def addKeywords(self, elements: str | List[str]):
        if isinstance(elements, str):
            self.keywords.append(elements)
        elif isinstance(elements, List[str]):
            self.keywords.extend(elements)
        else:
            raise TypeError("Input must be a string or a list of strings")
