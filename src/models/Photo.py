from typing import List
from Models.Base import Base


class Photo(Base):
    def __init__(self, path, keywords: List[str] | None):
        self.path = path
        self.keywords: List[str] = keywords | []

    def __str__(self):
        attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return ", ".join(attributes)

    def addKeywords(self, keyword: str | List[str]):
        if isinstance(keyword, str):
            self.keywords.append(keyword)
        elif isinstance(keyword, List[str]):
            self.keywords.extend(keyword)
        else:
            raise TypeError("Input must be a string or a list of strings")
