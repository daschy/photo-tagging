from sqlalchemy.ext.asyncio import AsyncEngine
from typing import List
from glob import glob
import os

# from sqlalchemy import create_engine
from models.orm.BaseOrm import BaseOrm


async def clear_tables(engine: AsyncEngine) -> None:
  async with engine.begin() as conn:
    await conn.run_sync(BaseOrm.metadata.drop_all)


def get_all_file_dir(directory_path: str, extension: str) -> List[str]:
  output = glob(
    os.path.join(directory_path, "**", f"*.{extension.lower()}"), recursive=True
  ) + glob(os.path.join(directory_path, "**", f"*.{extension.upper()}"), recursive=True)
  return output
