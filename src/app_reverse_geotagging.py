import asyncio

from models.ReverseGeotaggingXMP import ReverseGeotaggingXMP


async def main(file_path: str):
	geotagging_helper = ReverseGeotaggingXMP()
	address = await geotagging_helper.generate_reverse_geotag(file_path=file_path)
	print(address)


if __name__ == "__main__":
	image_path = "/Users/1q82/Pictures/Photos/Sport/Fencing/2022-NL-Camp/ZDS_3465.NEF"
	asyncio.run(main(image_path))
