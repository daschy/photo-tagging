from typing import List
from geopy.geocoders import Nominatim
from geopy.location import Location as GeopyLocation

from models.Base import Base
from models.ExifFileCRUD import ExifFileCRUD


class Location(Base):
	def __init__(self):
		self.city = None
		self.state = None
		self.country = None
		self.postal_code = None
		self.road = None


class ReverseGeotagging(Base):
	def __init__(self):
		super().__init__()
		self.exif_crud = ExifFileCRUD()
		self.geolocator = Nominatim(user_agent="reverse_geotagger")

	def _dms_to_decimal(self, dms_string):
		parts = dms_string.split(" ")
		degrees = float(parts[0])
		minutes = float(parts[2][:-1])
		seconds = float(parts[3][:-1])
		direction = parts[4]

		decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
		if direction in ["S", "W"]:
			decimal_degrees *= -1

		return decimal_degrees

	async def _get_gps_coordinates(
		self, file_path: str
	) -> tuple[float | None, float | None]:
		latitude_str, longitude_str = await self.exif_crud.read_gps_data(file_path)
		latitude = longitude = None
		if bool(latitude_str):
			latitude = self._dms_to_decimal(latitude_str)
		if bool(longitude_str):
			longitude = self._dms_to_decimal(longitude_str)
		return latitude, longitude

	def _reverse_geotag(self, latitude: float, longitude: float) -> Location | None:
		location: GeopyLocation = self.geolocator.reverse(
			(latitude, longitude),
			exactly_one=True,
			language="en",  # type: ignore
		)  # type: ignore

		if location:
			address_components = location.raw.get("address", {})

			result = Location()
			result.road = address_components.get("road", None)
			result.city = address_components.get("city", None)
			result.state = address_components.get("state", None)
			result.country = address_components.get("country", None)
			result.postal_code = address_components.get("postcode", None)

			return result
		else:
			return None

	async def generate_reverse_geotag(self, file_path) -> List[str]:
		lat, long = await self._get_gps_coordinates(file_path=file_path)
		if lat is None or long is None:
			output = []
		else:
			address: Location = self._reverse_geotag(lat, long)  # type: ignore
			output: List[str] = [
				x for x in [address.country, address.city, address.road] if x is not None
			]
		return output
