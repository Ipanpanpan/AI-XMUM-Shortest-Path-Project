import folium
import webbrowser
import folium.plugins
import folium.plugins.antpath
from pykml import parser
from folium.plugins import Search
from geopy.geocoders import Nominatim
from folium import Icon
import main_screen

def play(selected_location,current_coords):
    # Path to the KML file
    kml_file_path = 'AI shortest path project.kml'

    # Parse the KML file
    with open(kml_file_path, 'r') as file:
        root = parser.parse(file).getroot()

    # Extract names and coordinates, filtering out 'Untitled placemark'
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for placemark in root.Document.Placemark:
        name = placemark.name.text if hasattr(placemark, 'name') else None
        if name and name != 'Untitled placemark':  # Exclude 'Untitled placemark'
            coordinates = placemark.Point.coordinates.text.strip() if hasattr(placemark, 'Point') else None
            if coordinates:
                coords_tuple = list(map(float, coordinates.split(',')[:2]))  # Ignore altitude if present
                geojson_data["features"].append({
                    "type": "Feature",
                    "properties": {
                        "name": name  # Name property for search
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": coords_tuple  # GeoJSON format: [longitude, latitude]
                    }
                })



    # Create a map centered on the first coordinate or a default location
    if geojson_data["features"]:
        first_coords = geojson_data["features"][0]["geometry"]["coordinates"]
        m = folium.Map(location=[first_coords[1], first_coords[0]], zoom_start=17)
    else:
        m = folium.Map(location=[0, 0], zoom_start=2)

    # Add an empty GeoJSON layer for the Search plugin
    geojson_layer = folium.GeoJson(
        data=geojson_data,
        name="Markers",
        popup=folium.GeoJsonPopup(fields=["name"], labels=False),  # Show name in popup
        tooltip=folium.GeoJsonTooltip(fields=["name"], labels=False)  # Show name in tooltip
    )
    geojson_layer.add_to(m)
    
    folium.Marker(
    current_coords,
    popup="London",
    icon=Icon(color='red')  # You can choose 'green', 'blue', 'purple', etc.
    ).add_to(m)

    # Path
    # Define different locations if needed
    # Set current_position and to_location based on coordinates from the list
    current_position = geojson_data["features"][0]["geometry"]["coordinates"][::-1]  # Reverse order for [lat, lon]
    to_location = geojson_data["features"][10]["geometry"]["coordinates"][::-1]  # Second feature's coordinates
    shortest_path = [to_location,current_coords]


    # Add the AntPath with corrected parameters
    folium.plugins.AntPath(
        locations=shortest_path, reverse=True, dash_array=[10, 20]
    ).add_to(m)



    # Save the map to an HTML file
    map_file = "xmum_map.html"
    m.save(map_file)
    webbrowser.open(map_file)
    print(f"Map saved as {map_file}")
