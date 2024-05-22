import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.BaseOrm import BaseOrm
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.AIGenTokenClassificationBert import AIGenTokenClassificationBert
from src.models.AIGenPaliGemma import AIGenPaliGemma
from src.models.StrategyGenerateKeywordList import StrategyGenerateKeywordList


class TestStrategyGenerateKeywordList:
  strategy: StrategyGenerateKeywordList = None

  @classmethod
  def setup_class(cls):
    cls.strategy = StrategyGenerateKeywordList(
      image_to_text_ai=AIGenPaliGemma(model_id="google/paligemma-3b-ft-cococap-448"),
      token_classification_ai=AIGenTokenClassificationBert(
        model_id="vblagoje/bert-english-uncased-finetuned-pos",
      ),
      reverse_geotagging=ReverseGeotagging(),
    )
    cls.strategy.init()

  @pytest.mark.asyncio
  async def test_generate_keyword_list_image(self):
    image_path = f"{os.getcwd()}/src/tests/test_images/windmill_address_some_none.NEF"
    keyword_list = await self.strategy.generate_keyword_list_image(
      image_path=image_path
    )
    assert len(keyword_list) > 0
    assert [
      "Meester Jac. Takkade",
      "Netherlands",
      "background",
      "black",
      "blue",
      "sky",
      "white",
      "windmill",
    ] == keyword_list

  @pytest.mark.asyncio
  async def test_save_keyword_list_image(self):
    db_session, db_engine = await self.get_db_session()
    async with db_session() as db:
      image_path = f"{os.getcwd()}/src/tests/test_images/windmill_address_some_none.NEF"
      keyword_list = [
        "Meester Jac. Takkade",
        "Netherlands",
        "background",
        "black",
        "blue",
        "sky",
        "white",
        "windmill",
      ]
      save_output = await self.strategy.save(
        db, image_path=image_path, keyword_list=keyword_list
      )
    await self.clear_db(engine=db_engine)
    assert save_output

  async def get_db_session(
    self,
  ) -> [
    AsyncSession,
    AsyncEngine,
  ]:  # type: ignore
    db_path = f"sqlite+aiosqlite:////{os.getcwd()}/src/tests/test_images/test.db"
    db_engine: AsyncEngine = create_async_engine(db_path, echo=True)
    # Create the tables
    async with db_engine.begin() as conn:
      await conn.run_sync(BaseOrm.metadata.create_all)
    db_session = sessionmaker(
      bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )
    return db_session, db_engine

  async def clear_db(self, engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
      await conn.run_sync(BaseOrm.metadata.drop_all)
