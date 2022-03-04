# Importing the Nominatim geocoder class
from geopy.geocoders import Nominatim


def GetGeo(loc):
    # address we need to geocode
    #loc = 'the Apennine Mountains'

    # making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")

    # applying geocode method to get the location
    location = geolocator.geocode(loc)

    # printing address and coordinates

    if location is not None:
        print(location.address)
        print((location.latitude, location.longitude))
        return location

