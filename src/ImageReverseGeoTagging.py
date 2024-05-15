import exifread
from geopy.geocoders import Nominatim

from models.Location import Location

def get_gps_coordinates(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            latitude_ref = tags['GPS GPSLatitudeRef'].values
            longitude_ref = tags['GPS GPSLongitudeRef'].values
            latitude_values = tags['GPS GPSLatitude'].values
            longitude_values = tags['GPS GPSLongitude'].values
            
            # Convert GPS coordinates to decimal format
            latitude = float(latitude_values[0].num) / float(latitude_values[0].den)
            latitude += float(latitude_values[1].num) / (float(latitude_values[1].den) * 60)
            latitude += float(latitude_values[2].num) / (float(latitude_values[2].den) * 3600)
            if latitude_ref == 'S':
                latitude = -latitude
                
            longitude = float(longitude_values[0].num) / float(longitude_values[0].den)
            longitude += float(longitude_values[1].num) / (float(longitude_values[1].den) * 60)
            longitude += float(longitude_values[2].num) / (float(longitude_values[2].den) * 3600)
            if longitude_ref == 'W':
                longitude = -longitude
                
            return latitude, longitude
        else:
            return None

def reverse_geotag(latitude, longitude):
    geolocator = Nominatim(user_agent="reverse_geotagger")
    location = geolocator.reverse((latitude, longitude), exactly_one=True, language='en')
    
    if location:
        address_components = location.raw.get('address', {})
        
        result = Location()
        # result.address = location.address
        result.road = address_components.get('road', None)
        result.city = address_components.get('city', None)
        result.state = address_components.get('state', None)
        result.country = address_components.get('country', None)
        result.postal_code = address_components.get('postcode', None)
        
        return result
    else:
        return None

