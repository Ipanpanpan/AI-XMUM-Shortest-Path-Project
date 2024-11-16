import xml.etree.ElementTree as ET
import pandas as pd
from graph import Map

def parse_kml_to_dataframe(file_path: str) -> pd.DataFrame:
    # Step 1: Define the KML namespace
    namespace = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}

    # Step 2: Parse the KML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Step 3: Prepare a list to collect placemark data
    placemark_data = []

    # Step 4: Extract Placemarks from the Document
    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        # Extract the id of the Placemark
        placemark_id = placemark.get('id')

        # Extract the name of the Placemark
        name = placemark.find('kml:name', namespaces=namespace)
        name_text = name.text if name is not None else 'Unnamed'

        # Extract the styleUrl of the Placemark
        style_url = placemark.find('kml:styleUrl', namespaces=namespace)
        style_url_text = style_url.text if style_url is not None else 'No styleUrl'

        # Extract the coordinates of the Point element within the Placemark
        point = placemark.find('.//kml:Point', namespaces=namespace)
        coordinates = point.find('kml:coordinates', namespaces=namespace).text.strip() if point is not None else None

        # Append the data as a dictionary to the list
        placemark_data.append({
            'Placemark ID': placemark_id,
            'Name': name_text,
            'Style URL': style_url_text,
            'Coordinates': coordinates
        })

    # Step 5: Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(placemark_data)

    return df

# Example usage:
# Assuming 'example.kml' is the path to your KML file
file_path = 'data\AI shortest path project.kml'
df = parse_kml_to_dataframe(file_path)

# Display the DataFrame
print(df)


XMUM_map = Map()
XMUM_map.get_important_loc()

def get_map() -> Map:
    pass