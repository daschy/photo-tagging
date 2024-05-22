from logging import Logger

from src.utils.logger_utils import get_logger


class Base:
  def __init__(self):
    self.logger = get_logger(__name__)

  def __str__(self):
    attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
    return ", ".join(attributes)

  def __repr__(self):
    return self.__str__()
