import os
from typing import List
import asyncio
from src.models.Base import Base
import json


EXIF_TAG_KEYWORDS: str = "Keywords"
EXIF_TAG_IMAGEDESCRIPTION: str = "ImageDescription"


class ImageCRUD(Base):
  async def save_keyword_list(
    self, file_path, keyword_list: List[str], do_not_overwrite: bool = False
  ) -> bool:
    if not do_not_overwrite:
      await self.delete_all_keyword_list(file_path=file_path)
    process = await asyncio.create_subprocess_exec(
      "exiftool",
      *([f"-{EXIF_TAG_KEYWORDS}+={keyword}" for keyword in keyword_list]),
      file_path,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await process.communicate()

    if process.returncode != 0:
      raise ChildProcessError(f"ExifTool error: {stderr.decode().strip()}")

    # ExifTool creates a backup file with _original suffix, so remove it
    backup_file = f"{file_path}_original"
    if os.path.exists(backup_file):
      os.remove(backup_file)
    return True

  async def delete_all_keyword_list(self, file_path) -> bool:
    existing_keyword_list = await self.read_keyword_list(image_path=file_path)
    process = await asyncio.create_subprocess_exec(
      "exiftool",
      *([f"-{EXIF_TAG_KEYWORDS}-={keyword}" for keyword in existing_keyword_list]),
      file_path,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await process.communicate()

    if process.returncode != 0:
      raise ChildProcessError(f"ExifTool error: {stderr.decode().strip()}")

    # ExifTool creates a backup file with _original suffix, so remove it
    backup_file = f"{file_path}_original"
    if os.path.exists(backup_file):
      os.remove(backup_file)
    return True

  async def read_keyword_list(self, image_path) -> List[str]:
    process = await asyncio.create_subprocess_exec(
      "exiftool",
      f"-{EXIF_TAG_KEYWORDS}",
      "-json",
      image_path,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
      raise ChildProcessError(f"ExifTool error: {stderr.decode().strip()}")
    # Parse the JSON output
    exif_data = json.loads(stdout.decode())

    # Extract keywords from the EXIF data
    keyword_list = exif_data[0].get(EXIF_TAG_KEYWORDS, [])
    output: List[str] = keyword_list
    return output
