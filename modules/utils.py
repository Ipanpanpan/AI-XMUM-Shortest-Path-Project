from geopy.geocoders import Nominatim
import requests
from typing import Tuple
from location import Location

def get_curr_loc():
    try:
        # gets the public IP address
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip_address = ip_response.json()['ip']

        # uses Nominatim to get location information based on IP
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(ip_address)

        if location:
            return (location.latitude, location.longitude)  
        else:
            return None  
    except Exception as e:
        print(f"Error occurred: {e}")
        return None 


def main():
    print(get_curr_loc())

if __name__ == "__main__":
    main()