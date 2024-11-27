import geocoder
from typing import List, Tuple
from location import Location

def get_curr_loc() -> Tuple[float, float]:
    g = geocoder.ip('me')  # get location based on IP address
    if g.ok:
        return (g.latlng[0], g.latlng[1]) 
    else:
        return (None, None)  

if __name__ == "__main__":
    main()