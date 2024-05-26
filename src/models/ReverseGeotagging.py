import exifread
from typing import List
from geopy.geocoders import Nominatim

from models.Base import Base
from models.Location import Location


class ReverseGeotagging(Base):
  def _get_gps_coordinates(self, image_path):
    with open(image_path, "rb") as f:
      tags = exifread.process_file(f)
      if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
        latitude_ref = tags["GPS GPSLatitudeRef"].values
        longitude_ref = tags["GPS GPSLongitudeRef"].values
        latitude_values = tags["GPS GPSLatitude"].values
        longitude_values = tags["GPS GPSLongitude"].values

        # Convert GPS coordinates to decimal format
        latitude = float(latitude_values[0].num) / float(latitude_values[0].den)
        latitude += float(latitude_values[1].num) / (float(latitude_values[1].den) * 60)
        latitude += float(latitude_values[2].num) / (
          float(latitude_values[2].den) * 3600
        )
        if latitude_ref == "S":
          latitude = -latitude

        longitude = float(longitude_values[0].num) / float(longitude_values[0].den)
        longitude += float(longitude_values[1].num) / (
          float(longitude_values[1].den) * 60
        )
        longitude += float(longitude_values[2].num) / (
          float(longitude_values[2].den) * 3600
        )
        if longitude_ref == "W":
          longitude = -longitude

        return latitude, longitude
      else:
        return None, None

  def _reverse_geotag(self, latitude, longitude):
    geolocator = Nominatim(user_agent="reverse_geotagger")
    location = geolocator.reverse(
      (latitude, longitude), exactly_one=True, language="en"
    )

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

  async def generate_reverse_geotag(self, image_path) -> List[str]:
    lat, long = self._get_gps_coordinates(image_path=image_path)
    # self.logger.debug(f"start {image_path}: lat={lat},long={long}")
    if lat is None or long is None:
      output = []
    else:
      address = self._reverse_geotag(lat, long)
      output = [
        x for x in [address.country, address.city, address.road] if x is not None
      ]
    # self.logger.debug(f"end {image_path}: {output}")
    return output
