from typing import List
import uuid
from datetime import datetime
import pytz
from sqlalchemy import Column, UUID, String, JSON, DateTime
from src.Models.Base import Base
from src.Models.BaseOrm import BaseOrm


class Photo(Base, BaseOrm):
  __tablename__ = "Photos"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  path = Column(String, nullable=True, unique=True)
  filename = Column(String, nullable=True)
  keywordList = Column(JSON, nullable=True)
  createdAt = Column(DateTime, default=datetime.now(pytz.UTC))
  updatedAt = Column(
    DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC)
  )

  def __init__(self, path: str):
    self.path = path
    self.keywordList = []
    self.filename = path.split("/")[-1]

  def addKeywordList(self, keywordOrList: str | List[str]):
    if isinstance(keywordOrList, str):
      self.keywordList.append(keywordOrList)
    elif isinstance(keywordOrList, List):
      self.keywordList.extend(keywordOrList)
    else:
      raise TypeError("Input must be a string or a list of strings")

  def setKeywordList(self, keywordList: List[str]):
    self.keywordList = keywordList
