from typing import List
import uuid
from datetime import datetime
import pytz
from src.Models.BaseOrm import BaseOrm
from sqlalchemy import Column, UUID, String, JSON, DateTime
from src.Models.Base import Base


class Photo(Base, BaseOrm):
  __tablename__ = "Photos"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  path = Column(String, nullable=True, unique=True)
  filename = Column(String, nullable=True)
  keyword_list = Column(JSON, nullable=True)
  created_at = Column(DateTime, default=datetime.now(pytz.UTC))
  updated_at = Column(
    DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC)
  )

  def __init__(self, path: str):
    self.path = path
    self.keyword_list = []
    self.filename = path.split("/")[-1]

  def add_keyword_list(self, keyword_or_list: str | List[str]):
    if isinstance(keyword_or_list, str):
      self.keyword_list.append(keyword_or_list)
    elif isinstance(keyword_or_list, List):
      self.keyword_list.extend(keyword_or_list)
    else:
      raise TypeError("Input must be a string or a list of strings")

  def set_keyword_list(self, keyword_list: List[str]):
    self.keyword_list = keyword_list
