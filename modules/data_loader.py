import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from map import Map
from location import Location
from geopy.distance import geodesic

from map import find_nearest_location

def parse_path(file_path: str) -> pd.DataFrame:
    """
    Parses a KML file and extracts path segments as individual points with distances between them.

    Args:
        file_path (str): The path to the KML file containing path data.

    Returns:
        pd.DataFrame: A DataFrame containing the start and end points of each path segment, 
                      along with the distance between them in meters.
    """
    #Namespace for KML
    namespace = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    paths = []

    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        #Find LineString elements
        line_string = placemark.find('.//kml:LineString/kml:coordinates', namespaces=namespace)
        if line_string is not None:
            # print(f"Processing LineString: {line_string.text.strip()}")
            coords = line_string.text.strip().split()

            if len(coords) < 2:
                print(f"Skipped path due to insufficient coordinates: {coords}")
                continue

            #Store the coordinates as tuples (lat, lon)
            points = []
            for coord in coords:
                try:
                    lon, lat, *_ = map(float, coord.split(','))
                    points.append((lat, lon))  #Store as (lat, lon)
                except Exception as e:
                    print(f"Error parsing coordinate {coord}: {e}")
                    continue

            #Split the path into segments of consecutive points
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

    #Return the DataFrame with the individual segments
    return pd.DataFrame(paths)


def parse_location(file_path: str) -> pd.DataFrame:
    """
    Parses a KML file and extracts location data, including coordinates and importance status.

    Args:
        file_path (str): The path to the KML file containing location data.

    Returns:
        pd.DataFrame: A DataFrame containing the location ID, name, latitude, longitude, 
                      and importance status for each location.
    """
    #id, loc_name, latitude, longitude, is_important
    namespace = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    locations = []

    for idx, placemark in enumerate(root.findall('.//kml:Placemark', namespaces=namespace)):
        #Extract id
        loc_id = idx + 1

        #Extract name
        name = placemark.find('kml:name', namespaces=namespace)
        loc_name = name.text if name is not None else f"Location_{loc_id}"

        #Extract coordinates
        point = placemark.find('.//kml:Point/kml:coordinates', namespaces=namespace)
        if point is not None:
            coordinates = point.text.strip()
            lon, lat, *_ = map(float, coordinates.split(','))

            #Check the <styleUrl> tag to determine if the location is important
            style_url = placemark.find('kml:styleUrl', namespaces=namespace)
            style_url_text = style_url.text if style_url is not None else ''

            is_important = style_url_text != '#__managed_style_0D431BAC7434B0BBDE51'  #Important if not matching the "not important" style


            locations.append({
                'id': loc_id,
                'loc_name': loc_name,
                'latitude': lat,
                'longitude': lon,
                'is_important': is_important
            })

    return pd.DataFrame(locations)



def validate_kml(file_path: str, location_df: pd.DataFrame, path_df: pd.DataFrame):
    """
    Validates the KML file by comparing the location and path data in the file with the provided DataFrames.

    Args:
        file_path (str): The path to the KML file containing the location and path data.
        location_df (pd.DataFrame): A DataFrame containing the expected location data.
        path_df (pd.DataFrame): A DataFrame containing the expected path segment data.

    Raises:
        AssertionError: If the number of locations or path segments in the KML does not match the DataFrame.
    """
    namespace = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    #Validate locations
    kml_locations = []
    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        point = placemark.find('.//kml:Point/kml:coordinates', namespaces=namespace)
        if point is not None:
            kml_locations.append(point.text.strip())

    assert len(kml_locations) == len(location_df), "Mismatch in number of locations"
    print("Location validation passed!")

    #Validate paths
    kml_segments = []  #List to store individual path segments

    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        line_string = placemark.find('.//kml:LineString/kml:coordinates', namespaces=namespace)
        if line_string is not None:
            coords = line_string.text.strip().split()

            #If there are multiple coordinates, divide them into segments
            if len(coords) > 1:
                for i in range(len(coords) - 1):
                    #Split each pair of coordinates and append to kml_segments
                    start_coords = coords[i].split(',')
                    end_coords = coords[i + 1].split(',')
                    start_point = (float(start_coords[1]), float(start_coords[0]))  #(lat, lon)
                    end_point = (float(end_coords[1]), float(end_coords[0]))  #(lat, lon)
                    kml_segments.append((start_point, end_point))
            else:
                #Single point path, append as a segment if needed
                start_coords = coords[0].split(',')
                start_point = (float(start_coords[1]), float(start_coords[0]))  #(lat, lon)
                kml_segments.append((start_point, start_point))  #Single point segment

    #Now compare the number of segments in the KML with the number of rows in the DataFrame
    assert len(kml_segments) == len(path_df), f"Mismatch in number of segments: KML={len(kml_segments)}, DataFrame={len(path_df)}"
    print("Path validation passed!")


def get_map() -> Map:
    """
    Generates a map by parsing location and path data from a KML file and adding locations and paths to the map.

    Returns:
        Map: A Map object containing all the locations and paths parsed from the KML file.
    """
    file_path = r"data\AI shortest path project.kml"
    location_df = parse_location(file_path)
    path_df = parse_path(file_path)

    XMUM_map = Map()
    
    for _, row in location_df.iterrows():
        loc = Location(
            name=row['loc_name'].strip(),
            latitude=row['latitude'],
            longitude=row['longitude'],
            id=row['id'],
            is_important=row['is_important']
        )
        XMUM_map.add_loc(loc)

    locs_coor = np.array([[loc.get_latitude(), loc.get_longitude()] for loc in XMUM_map.get_all_loc()])
    for _, row in path_df.iterrows():
        start_coords = row['start_point']
        end_coords = row['end_point']

        start_loc : Location = find_nearest_location(start_coords, XMUM_map, locs_coor)
        end_loc : Location = find_nearest_location(end_coords, XMUM_map, locs_coor)

        distance = geodesic(start_loc.get_coordinate(), end_loc.get_coordinate()).meters

        XMUM_map.add_path(start_loc.get_id(), end_loc.get_id(), distance)
        
    return XMUM_map


def main():
    """
    The main entry point for the script. It parses location and path data from a KML file, validates the data, 
    and prints the important locations and other details about the map.

    Runs the KML file parsing, validation, and map creation, then prints the sorted list of important locations 
    and the number of locations and paths.
    """
    file_path = r"data\AI shortest path project.kml"
    location_df = parse_location(file_path)
    path_df = parse_path(file_path)
    print("Location DataFrame: ")
    #print(location_df.head())
    #print("Path DataFrame: ")
    #print(path_df.head())
    validate_kml(file_path, location_df, path_df)
    
    xmum : Map = get_map()
    #print([x.get_name() for x in xmum.get_important_loc()])
    #print(location_df)
    print(sorted([loc.get_name() for loc in (xmum.get_important_loc())]))
    print(len(xmum.get_all_loc()))
    print(len(path_df))

if __name__ == "__main__":
    main()
