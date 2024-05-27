from abc import abstractmethod
from typing import Generic, Tuple, TypeVar
import torch

from transformers import PreTrainedModel, ProcessorMixin, AutoTokenizer

from models.Base import Base

ModelT = TypeVar("ModelT", bound=PreTrainedModel)
ProcessorT = TypeVar("ProcessorT", bound=ProcessorMixin | AutoTokenizer)


class AIGen(Base, Generic[ModelT, ProcessorT]):
	def __init__(self, model_id: str):
		super().__init__()
		self.model_id = model_id
		self.device = "cuda" if torch.cuda.is_available() else "cpu"

	@abstractmethod
	def ai_init(self) -> None:
		pass

	@abstractmethod
	def is_init(
		self,
	) -> bool:
		pass
