from logging import INFO
import os
import asyncio
from src.models.AIGenPretrained import AIGenPretrained
from src.models.AIGenPipeline import AIGenPipeline
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.StrategyGenerateKeywordList import StrategyGenerateKeywordList


async def main(root_dir: str):
  strategy = StrategyGenerateKeywordList(
    image_to_text_ai=AIGenPretrained(
      model_id="google/paligemma-3b-ft-cococap-448",
    ),
    token_classification_ai=AIGenPipeline(
      model_id="vblagoje/bert-english-uncased-finetuned-pos",
    ),
    reverse_geotagging=ReverseGeotagging(),
    db_path=f"sqlite+aiosqlite:////{os.getcwd()}/prod_paligemma-3b-ft-cococap.db",
  )
  await strategy.init()
  await strategy.generate_keyword_list_directory(root_dir=root_dir)


if __name__ == "__main__":
  directory = "/Users/1q82/Pictures/Photos/Amsterdam"
  asyncio.run(main(directory))
