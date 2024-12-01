# main.py
from typing import Optional
from typing import Tuple
from map import Map
from typing import List
from location import Location
from geopy.distance import geodesic
import numpy as np

import matplotlib.pyplot as plt


from data_loader import get_map

import random

def main():
    
    # Initialize Map
    city_map = Map()
    # random.seed(90)
    # for i in range(100):
    #     x, y = random.uniform(0, 10), random.uniform(0, 10)
    #     loc_i : Location = Location(id = str(i), name = str(i), latitude= x, longitude= y, is_important= True)
    #     city_map.add_loc(loc_i)
    #     n_neighbour = random.randint(1, 2)
    #     for j in range(n_neighbour):
    #         loc2 = random.choice(city_map.get_all_loc())
    #         # dis = (sum((k_1 - k_2) ** 2 for k_1, k_2 in 
    #         #            zip(loc_i.get_coordinate(), loc2.get_coordinate()))) ** (1/2)
    #         dis = geodesic(loc_i.get_coordinate(), loc2.get_coordinate()).meters
    #         city_map.add_path(loc_i.get_id(), loc2.get_id(), dis)
    xmum_map = get_map()

    city_map = xmum_map
    # Test Shortest Paths
    start_location = "LY8"  # New York
    end_location = "Entrance Gate"     # Los Angeles
    

    print(f"Finding shortest path from {start_location} to {end_location}...")
    path, distance = city_map.shortest_path(from_loc=start_location, to_loc=end_location, search_algorithm= "iterative deepening")
    # path, distance = [], 10
    if path:
        print("Shortest path coordinates:")
        for coord in path:
            print(coord)
    else:
        print("No path found.")
    print(f"total distance : {distance}")
    # Visualization
    visualize_map(city_map, path, start_location, end_location)

def visualize_map(city_map: Map, path: Optional[List[Tuple[float, float]]], start_name: str, end_name: str, path_on = True, text_on= True):
    # Create a plot
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # Plot all paths
    if path_on:
        for loc in city_map.get_all_loc():
            x_start, y_start   = loc.get_longitude(), loc.get_latitude()
            for path_i in loc.get_neighbouring_path():
                neighbor = path_i.get_end_loc()
                x_end, y_end  = neighbor.get_longitude(), neighbor.get_latitude()
                plt.plot([x_start, x_end], [y_start, y_end], 'lightgray', linewidth=1, zorder=1)

    # Plot all locations
    for loc in city_map.get_all_loc():
        y, x = loc.get_longitude(), loc.get_latitude()
        if loc.get_name() == start_name:
            plt.scatter(y,x, color='green', s=100, zorder=2, label='Start')
        elif loc.get_name() == end_name:
            plt.scatter(y, x, color='red', s=100, zorder=2, label='End')
        else:
            plt.scatter(y, x, color='blue', s=50, zorder=2)
        if text_on and loc.is_important():
            plt.text(y + 0.00005, x + 0.00005, loc.get_name(), fontsize=9, zorder=3)

    # Highlight the shortest path
    if path:
        path_lons = [coord[1] for coord in path]  # Longitude
        path_lats = [coord[0] for coord in path]  # Latitude
        plt.plot(path_lons,path_lats, color='orange', linewidth=3, label='Shortest Path', zorder=4)

    # Set labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Map of Locations and Shortest Path')

    # Create a legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    # Show grid
    plt.grid(True, linestyle='--', alpha=0.5)

    # Show the plot
    plt.show()

if __name__ == "__main__":
        main()