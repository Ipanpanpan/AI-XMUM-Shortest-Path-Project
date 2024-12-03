import requests
from typing import List, Tuple
from location import Location

def get_curr_loc() -> Tuple[float, float]:
    """this function fetches the current geolocation of the user based on their public IP address."""
    # Send a GET request to ipinfo.io to get geolocation data based on the public IP
    try:
        response = requests.get('http://ipinfo.io/json')
        data = response.json()

        # Extract the location (latitude and longitude)
        loc = data.get('loc', '').split(',')
        if len(loc) == 2:
            latitude = float(loc[0])
            longitude = float(loc[1])
            return latitude, longitude
        else:
            raise ValueError("Location data is incomplete or invalid.")

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching location: {e}")
        return None


def main():
    print(get_curr_loc())


if __name__ == "__main__":
    main()
