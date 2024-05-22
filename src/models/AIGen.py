from abc import abstractmethod
from typing import Generic, Tuple, TypeVar
import torch

from transformers import PreTrainedModel, ProcessorMixin, AutoTokenizer, Pipeline

from src.models.Base import Base
from src.utils.logger_utils import get_logger

ModelT = TypeVar("ModelT", bound=PreTrainedModel)
ProcessorT = TypeVar("ProcessorT", bound=ProcessorMixin | AutoTokenizer)


class AIGen(Base, Generic[ModelT, ProcessorT]):
  def __init__(self, model_id: str):
    self.model_id = model_id
    self.model: ModelT = None
    self.processor: ProcessorT = None
    self.pipeline: Pipeline = None
    self.logger = get_logger(__name__)
    self.device = "cuda" if torch.cuda.is_available() else "cpu"

  @abstractmethod
  def ai_init(self) -> Tuple[ModelT, ProcessorT]:
    pass
