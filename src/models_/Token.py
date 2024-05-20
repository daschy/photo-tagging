from src.Models_.Base import Base

class Token(Base):
    def __init__(self, text, score, label):
        self.text = text
        self.score = score
        self.label = label

    def __repr__(self):
        return f"Entity(text={self.text!r}, score={self.score}, label={self.label!r})"