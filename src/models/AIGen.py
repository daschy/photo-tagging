from abc import abstractmethod
from typing import Generic, TypeVar, List, TypedDict
from typing_extensions import Unpack, Required
import torch

from transformers import PreTrainedModel, ProcessorMixin, AutoTokenizer

from models.Base import Base


class AIGenParams(TypedDict):
	text: Required[str]


ModelT = TypeVar("ModelT", bound=PreTrainedModel)
ProcessorT = TypeVar("ProcessorT", bound=ProcessorMixin | AutoTokenizer | None)
ParamsT = TypeVar("ParamsT", bound=AIGenParams)


class AIGen(Base, Generic[ParamsT]):
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

	@abstractmethod
	async def generate(self, **kwargs: Unpack[ParamsT]) -> str | List[str]:
		pass
