from prettyprinter import cpprint as pp
from reversegeotagging import get_gps_coordinates, reverse_geotag
from ImageKeywords import captionListToKeywords
from ImageCaptionGenerate import generateCaptionList


# Example usage
image_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"

image_caption_list = generateCaptionList(image_path)
keywords = captionListToKeywords([item.caption for item in image_caption_list])
coordinates = get_gps_coordinates(image_path)
if coordinates:
    print("GPS Coordinates:", coordinates)
else:
    print("No GPS coordinates found in the image EXIF data.")

latitude = coordinates[0]  # Example latitude
longitude = coordinates[1]

address = reverse_geotag(latitude, longitude)
if address:
    print(address)
else:
    pp("No address found for the provided coordinates.")


pp([address.country, address.city, address.road] + keywords)
