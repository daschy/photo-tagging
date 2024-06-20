import uuid
from datetime import datetime
import pytz
from sqlalchemy import Column, UUID, String, JSON, DateTime
from models.orm.BaseOrm import BaseOrm


class Image(BaseOrm):
	__tablename__ = "Images"
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	file_path = Column(String, nullable=True, unique=True)
	file_name = Column(String, nullable=True)
	keyword_list_description = Column(JSON, nullable=True)
	keyword_list_address = Column(JSON, nullable=True)

	created_at = Column(
		DateTime,
		default=lambda: datetime.now(pytz.UTC),
	)
	updated_at = Column(
		DateTime,
		default=lambda: datetime.now(pytz.UTC),
		onupdate=lambda: datetime.now(pytz.UTC),
	)

	def __init__(self, file_path: str):
		super().__init__()
		self.file_path = file_path
		self.file_name = file_path.split("/")[-1]

	def set_keyword_list_description(
		self, keyword_list_description: list[str]
	) -> "Image":
		self.keyword_list_description = keyword_list_description
		return self
