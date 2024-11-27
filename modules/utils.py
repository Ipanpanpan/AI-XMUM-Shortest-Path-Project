import requests
from typing import Tuple
from location import Location

def get_curr_loc() -> Tuple[float, float]:
    try:
        # gets the public IP address
        ip_response = requests.get('https://api.ipify.org?format=json')
        ip_address = ip_response.json()['ip']

        # use IP geolocation service to get location information based on IP
        geo_response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        geo_data = geo_response.json()

        if 'latitude' in geo_data and 'longitude' in geo_data:
            return (geo_data['latitude'], geo_data['longitude'])  
        else:
            return None  
    except Exception as e:
        print(f"Error occurred: {e}")
        return None 


def main():
    print(get_curr_loc())

if __name__ == "__main__":
    main()