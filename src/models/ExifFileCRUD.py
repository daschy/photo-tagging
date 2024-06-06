from asyncio.subprocess import Process
import os
from typing import List
import asyncio
from models.Base import Base
import json


_EXIF_TAG_KEYWORDS = "Keywords"
_EXIF_TAG_GPS_LATITUDE = "GPSLatitude"
_EXIF_TAG_GPS_LONGITUDE = "GPSLongitude"


class ExifFileCRUD(Base):
	async def save_keyword_list(self, file_path, keyword_list: List[str]) -> bool:
		await self._execute_exiftool(
			([f"-{_EXIF_TAG_KEYWORDS}={keyword}" for keyword in keyword_list] + ["-json"]),
			file_path,
		)
		return True

	async def add_keyword_list(self, file_path, keyword_list: List[str]) -> bool:
		await self._execute_exiftool(
			([f"-{_EXIF_TAG_KEYWORDS}+={keyword}" for keyword in keyword_list] + ["-json"]),
			file_path,
		)
		return True

	async def delete_keyword_list(self, file_path: str) -> bool:
		await self._execute_exiftool(
			args=[f"-{_EXIF_TAG_KEYWORDS}=", "-json"],
			file_path=file_path,
		)
		return True

	async def delete_gps_data(self, file_path: str) -> bool:
		await self._execute_exiftool(
			args=[f"-{_EXIF_TAG_GPS_LATITUDE}=", f"-{_EXIF_TAG_GPS_LONGITUDE}=", "-json"],
			file_path=file_path,
		)
		return True

	async def read_keyword_list(self, file_path) -> List[str]:
		exif_data = await self._execute_exiftool(
			args=[f"-{_EXIF_TAG_KEYWORDS}", "-json"],
			file_path=file_path,
		)
		return exif_data[0].get(_EXIF_TAG_KEYWORDS, [])

	async def save_gps_data(self, file_path: str, lat: str, lon: str) -> bool:
		await self._execute_exiftool(
			args=[
				f"-{_EXIF_TAG_GPS_LATITUDE}*={lat}",
				f"-{_EXIF_TAG_GPS_LONGITUDE}*={lon}",
				"-json",
			],
			file_path=file_path,
		)
		return True

	async def save_gps_data_decimal(self, file_path: str, lat: float, lon: float) -> bool:
		await self.save_gps_data(file_path=file_path, lat=f"{lat}", lon=f"{lon}")
		return True

	async def read_gps_data(self, file_path: str) -> tuple[str, str]:
		exif_data = await self._execute_exiftool(
			args=[f"-{_EXIF_TAG_GPS_LATITUDE}", f"-{_EXIF_TAG_GPS_LONGITUDE}", "-json"],
			file_path=file_path,
		)
		latitude_ref = exif_data[0].get(_EXIF_TAG_GPS_LATITUDE, "")
		longitude_ref = exif_data[0].get(_EXIF_TAG_GPS_LONGITUDE, "")
		return latitude_ref, longitude_ref

	async def _execute_exiftool(self, args: List[str], file_path: str) -> dict:
		try:
			process: Process = await asyncio.create_subprocess_exec(
				"exiftool",
				*args,
				file_path,
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.PIPE,
			)
			stdout, stderr = await process.communicate()
			if process.returncode != 0:
				raise ChildProcessError(f"ExifTool error: {stderr.decode().strip()}")
			backup_file = f"{file_path}_original"
			if os.path.exists(backup_file):
				os.remove(backup_file)

			# if bool(stderr.decode()):
			# 	raise ChildProcessError(stderr.decode())

			if not bool(stdout.decode()):
				return {}
			return json.loads(stdout.decode())

		except json.JSONDecodeError as e:
			raise e
		except ChildProcessError as e:
			raise e
