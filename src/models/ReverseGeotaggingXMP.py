import os
from models.ReverseGeotagging import ReverseGeotagging


class ReverseGeotaggingXMP(ReverseGeotagging):
	async def _get_gps_coordinates(self, file_path) -> tuple[float | None, float | None]:
		file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
		file_path_xmp = os.path.join(
			os.path.dirname(file_path),
			file_name_without_ext + ".xmp",
		)
		if os.path.exists(file_path_xmp):
			lat_str, lon_str = await self.exif_crud.read_gps_data(file_path_xmp)
			lat = lon = None
			if bool(lat_str):
				lat = self._dms_to_decimal(lat_str)
			if bool(lon_str):
				lon = self._dms_to_decimal(lon_str)
			return lat, lon
		else:
			return await super()._get_gps_coordinates(file_path=file_path)  # type: ignore
