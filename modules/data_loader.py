import xml.etree.ElementTree as ET
import pandas as pd
from map import Map
from location import Location
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
            # print(f"Processing LineString: {line_string.text.strip()}")
            coords = line_string.text.strip().split()

            if len(coords) < 2:
                print(f"Skipped path due to insufficient coordinates: {coords}")
                continue

            # Store the coordinates as tuples (lat, lon)
            points = []
            for coord in coords:
                try:
                    lon, lat, *_ = map(float, coord.split(','))
                    points.append((lat, lon))  # Store as (lat, lon)
                except Exception as e:
                    print(f"Error parsing coordinate {coord}: {e}")
                    continue

            # Split the path into segments of consecutive points
            for i in range(len(points) - 1):
                start_point = points[i]
                end_point = points[i + 1]
                distance = geodesic(start_point, end_point).meters
                # print(f"Start Point: {start_point}, End Point: {end_point}, Distance: {distance}")
                paths.append({
                    'start_point': start_point,
                    'end_point': end_point,
                    'distance': distance
                })

    # Return the DataFrame with the individual segments
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
            is_important = style_url_text != '#__managed_style_0AFAFFDB3434A1AD5DE3'  # Important if not matching the "not important" style

            locations.append({
                'id': loc_id,
                'loc_name': loc_name,
                'latitude': lat,
                'longitude': lon,
                'is_important': is_important
            })

    return pd.DataFrame(locations)



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
    kml_segments = []  # List to store individual path segments

    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        line_string = placemark.find('.//kml:LineString/kml:coordinates', namespaces=namespace)
        if line_string is not None:
            coords = line_string.text.strip().split()
            
            # If there are multiple coordinates, divide them into segments
            if len(coords) > 1:
                for i in range(len(coords) - 1):
                    # Split each pair of coordinates and append to kml_segments
                    start_coords = coords[i].split(',')
                    end_coords = coords[i + 1].split(',')
                    start_point = (float(start_coords[1]), float(start_coords[0]))  # (lat, lon)
                    end_point = (float(end_coords[1]), float(end_coords[0]))  # (lat, lon)
                    kml_segments.append((start_point, end_point))
            else:
                # Single point path, append as a segment if needed
                start_coords = coords[0].split(',')
                start_point = (float(start_coords[1]), float(start_coords[0]))  # (lat, lon)
                kml_segments.append((start_point, start_point))  # Single point segment

    # Now compare the number of segments in the KML with the number of rows in the DataFrame
    assert len(kml_segments) == len(path_df), f"Mismatch in number of segments: KML={len(kml_segments)}, DataFrame={len(path_df)}"
    print("Path validation passed!")








def get_map() -> Map:
    file_path = r"data\AI shortest path project.kml"
    location_df = parse_location(file_path)
    path_df = parse_path(file_path)

    XMUM_map = Map()
    location_objects = {}
    
    for _, row in location_df.iterrows():
        loc = Location(
            name = row['loc_name'],
            latitude = row['latitude'],
            longitude = row['longitude'],
            id = row['id'],
            is_important = row['is_important']
        )
        XMUM_map.add_loc(loc)
        location_objects[(row['latitude'], row['longitude'])] = loc
    
    for _, row in path_df.iterrows():
        start_coords = row['start_point']
        end_coords = row['end_point']
        distance = row['distance']

        start_loc = location_objects.get(start_coords)
        end_loc = location_objects.get(end_coords)

        if start_loc and end_loc:
            start_loc.add_neighbouring_path(end_loc, distance)
            end_loc.add_neighbouring_path(start_loc, distance)
    
    return XMUM_map



def main():
    
    file_path = r"data\AI shortest path project.kml"
    location_df = parse_location(file_path)
    path_df = parse_path(file_path)
    print("Location DataFrame: ")
    # print(location_df.head())
    # print("Path DataFrame: ")
    # print(path_df.head())
    validate_kml(file_path, location_df, path_df)
    xmum : Map= get_map()
    # print([x.get_name() for x in xmum.get_important_loc()])
    # print(location_df)
    print(location_df.loc_name[location_df.is_important == True])
if __name__ == "__main__":
    main()