from abc import ABC
from logging import Logger

from utils.logger_utils import get_logger


class Base(ABC):
	def __init__(self):
		class_name: str = f"{type(self)}"
		self.logger: Logger = get_logger(f"{class_name.split('.')[-1]}")

	def __str__(self):
		attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
		return ", ".join(attributes)

	def __repr__(self):
		return self.__str__()
