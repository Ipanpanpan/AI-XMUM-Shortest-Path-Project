import folium
import webbrowser
import folium.plugins
from pykml import parser
from folium.plugins import Search
from flask import Flask, request, jsonify
import threading
import time

XMUM_map = get_map()



# Initialize Flask app
app = Flask(__name__)

# Initialize a variable to hold received coordinates
received_coordinates = []

# Route to receive coordinates from JavaScript
@app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    global received_coordinates
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Update the global variable with the new coordinates
    received_coordinates = (latitude, longitude)
    
    # Print the coordinates to check in real-time
    print(f"Received coordinates: {received_coordinates}")
    
    return jsonify({"status": "Coordinates updated successfully!"}), 200

# Function to run Flask in a background thread
def run_flask():
    app.run(host='0.0.0.0', port=59957)

# Start Flask server in a background thread to avoid blocking the rest of the program
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

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

# If you want to get the user device position after loading the map, set auto_start=True
locate = folium.plugins.LocateControl(auto_start=True).add_to(m)

# Add a search bar linked to the GeoJSON layer
search = Search(
    layer=geojson_layer,
    geom_type="Point",
    placeholder="Search by name",
    collapsed=False,  # Keep the search bar visible
    search_label="name"  # Link search to the 'name' property
)
search.add_to(m)

# Add JavaScript to send coordinates to the Python server on location found
search_control = """
    <script type="text/javascript">
        var searchControl = document.querySelector('.leaflet-control-search');
        searchControl.addEventListener('search:locationfound', function(e) {
            var latLng = e.latlng;
            var coordinates = {
                latitude: latLng.lat,
                longitude: latLng.lng
            };

            // Send coordinates to Python server using fetch API
            fetch('http://localhost:59957/update_coordinates', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(coordinates),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Coordinates sent to server:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });

            // Open popup if it exists
            if (e.layer._popup) e.layer.openPopup();
        });
    </script>
"""

# Insert the JavaScript into the map HTML
m.get_root().html.add_child(folium.Element(search_control))

# Save the map to an HTML file
map_file = "map_with_search_to_show_markers.html"
m.save(map_file)
webbrowser.open(map_file)
print(f"Map saved as {map_file}")

# Keep the program running while the Flask server is up
while True:
    time.sleep(1)  # Keep the main thread alive to keep the server running
    print(received_coordinates)