import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from src.models.PhotoKeywordContext import PhotoKeywordContext
from src.models.StrategySaveKeywordOnlyDB import StrategySaveKeywordOnlyDB
from src.utils.db_utils import init_db, AsyncSessionLocal
from src.utils.logger_utils import get_logger


log = get_logger(__name__)


async def process_image(context: PhotoKeywordContext, image_path: str):
  # loop = asyncio.get_event_loop()
  # await loop.run_in_executor(executor, context.add_keywords, image_path)
  await context.add_keywords(image_path=image_path)


async def main(root_dir: str):
  await init_db()
  async with AsyncSessionLocal() as db:
    # Initialize the context with a concrete strategy
    context = PhotoKeywordContext(StrategySaveKeywordOnlyDB(log, db))
    # executor = ThreadPoolExecutor()
    extensions = [".png", ".jpg", ".jpeg", ".tiff", ".nef"]
    # with ThreadPoolExecutor() as executor:
    for subdir, _, files in os.walk(root_dir):
      for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
          filename = f"{subdir}/{file}".replace("//", "/")
          await process_image(context=context, image_path=filename)

    # await asyncio.gather(*tasks_list)


if __name__ == "__main__":
  directory = "/Users/1q82/Pictures/Photos/Amsterdam"
  asyncio.run(main(directory))
