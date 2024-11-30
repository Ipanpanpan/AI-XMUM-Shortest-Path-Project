from map import Map
from data_loader import get_map
import folium
import webbrowser
import folium.plugins
import folium.plugins.antpath
import math
from data_loader import find_nearest_location

def play(from_location,to_location):
    xmu = Map()
    xmu = get_map()
    # Get a list of important locations
    important_locations = xmu.get_important_loc()
    print(from_location, to_location)
    shortest_path, distance = xmu.shortest_path([2.834845, 101.702392], to_loc=to_location)
    # Create a dictionary mapping names to coordinates
    locations_dict = {loc.get_name(): loc.get_coordinate() for loc in important_locations}

    # Define Map Center and Create Map
    map_center = [2.832818, 101.705657]  # Example coordinates (Kuala Lumpur)
    m = folium.Map(location=map_center, zoom_start=17)


    from_group = folium.FeatureGroup(name="Current Location", control=True)
    to_group = folium.FeatureGroup(name="To Locations", control=True)
    other_group = folium.FeatureGroup(name="Other Important Locations", control=True, show=False)


    for name, coord in locations_dict.items():
        if name == to_location:
            folium.Marker(
                location=coord,
                tooltip=f"To: {name}",
                icon=folium.Icon(color='green',prefix='fa',icon='arrow-down'),
            ).add_to(to_group)
        else:
            folium.Marker(
                location=coord,
                tooltip=name,
                icon=folium.Icon(color='gray',prefix='fa',icon='circle'),
    ).add_to(other_group)
        folium.Marker(
        location=from_location,
        tooltip="Current Position",
        icon=folium.Icon(color='blue',prefix='fa',icon='arrow-up'),
    ).add_to(from_group)
    # Add Groups to Map
    from_group.add_to(m)
    to_group.add_to(m)
    other_group.add_to(m)



    folium.plugins.AntPath(
        locations=shortest_path, reverse=False, dash_array=[10, 20], popup=f"Distance: {math.floor(distance)} m"
    ).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    # Save Map and Open in Browser
    map_file = "xmum_map.html"
    m.save(map_file)
    webbrowser.open(map_file)
    print(f"Map saved as {map_file}")