import xml.etree.ElementTree as ET
import pandas as pd
#from map import Map
#from location import Location
from geopy.distance import geodesic

def parse_path(file_path: str) -> pd.DataFrame:
    # Namespace for KML
    namespace = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    paths = []


    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        # Find LineString elements
        line_string = placemark.find('.//kml:LineString/kml:coordinates', namespaces=namespace)
        if line_string is not None:
            print(f"Processing LineString: {line_string.text.strip()}")
            coords = line_string.text.strip().split()
            
            if len(coords) < 2:
                print(f"Skipped path due to insufficient coordinates: {coords}")
                continue

            for i in range(len(coords) - 1):
                try:
                    start_coords = coords[i].split(',')
                    end_coords = coords[i + 1].split(',')

                    start_point = (float(start_coords[1]), float(start_coords[0]))
                    end_point = (float(end_coords[1]), float(end_coords[0]))
                    distance = geodesic(start_point, end_point).kilometers
                    print(f"Start Point: {start_point}, End Point: {end_point}, Distance: {distance}")
                    paths.append({
                        'start_point': start_point,
                        'end_point': end_point,
                        'distance': distance
                    })
                except Exception as e:
                    print(f"Error parsing path segment: {coords[i]} to {coords[i + 1]} - {e}")

    # Return the DataFrame
    return pd.DataFrame(paths)




def parse_location(file_path: str) -> pd.DataFrame:
    # id, loc_name, latitude, longitude, is_important
    namespace = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    locations = []

    for idx, placemark in enumerate(root.findall('.//kml:Placemark', namespaces=namespace)):
        # Extract id
        loc_id = idx + 1

        # Extract name
        name = placemark.find('kml:name', namespaces=namespace)
        loc_name = name.text if name is not None else f"Location_{loc_id}"

        # Extract coordinates
        point = placemark.find('.//kml:Point/kml:coordinates', namespaces=namespace)
        if point is not None:
            coordinates = point.text.strip()
            lon, lat, *_ = map(float, coordinates.split(','))

            # Check the <styleUrl> tag to determine if the location is important
            style_url = placemark.find('kml:styleUrl', namespaces=namespace)
            style_url_text = style_url.text if style_url is not None else ''
            is_important = style_url_text != '#__managed_style_34B45FA3D13474D10863'  # Important if not matching the "not important" style

            locations.append({
                'id': loc_id,
                'loc_name': loc_name,
                'latitude': lat,
                'longitude': lon,
                'is_important': is_important
            })

    return pd.DataFrame(locations)

file_path = r"C:\Users\Ivan Nathanael\AI-XMUM-Shortest-Path-Project\data\AI shortest path project.kml"

location_df = parse_location(file_path)
path_df = parse_path(file_path)
print("Location DataFrame: ")
print(location_df.head())
print("Path DataFrame: ")
print(path_df.head())

def validate_kml(file_path: str, location_df: pd.DataFrame, path_df: pd.DataFrame):
    namespace = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Validate locations
    kml_locations = []
    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        point = placemark.find('.//kml:Point/kml:coordinates', namespaces=namespace)
        if point is not None:
            kml_locations.append(point.text.strip())

    assert len(kml_locations) == len(location_df), "Mismatch in number of locations"
    print("Location validation passed!")

    # Validate paths
    kml_paths = []
    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        line_string = placemark.find('.//kml:LineString/kml:coordinates', namespaces=namespace)
        if line_string is not None:
            kml_paths.append(line_string.text.strip())

    assert len(kml_paths) == len(path_df), f"Mismatch in number of paths: KML={len(kml_paths)}, DataFrame={len(path_df)}"
    print("Path validation passed!")


validate_kml(file_path, location_df, path_df)





'''
def get_map() -> Map:
    XMUM_map = Map()
    loc = Location()
    XMUM_map.add_loc(loc)

    return XMUM_map
'''