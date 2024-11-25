from typing import Dict, List
from location import Location, Path
from geopy.distance import geodesic
from queue import PriorityQueue


class Map: 
    def __init__(self):
        self.__nodes : Dict[str : Location] = {}
    
    def add_loc(self, loc : Location):
        self.__nodes[loc.get_id()] = loc
    
    def del_loc(self, id : str):
        del self.__nodes[id]
    
    def get_imp_loc_id_mapping(self) -> Dict[str, str]:
        loc_id = {}
        important_loc = self.get_important_loc()
        for loc in important_loc:
            loc_id[loc.get_name()] = loc.get_id()
        return loc_id
    
    def get_all_loc(self) -> List[Location]:
        return self.__nodes.values()
    
    def get_important_loc(self) -> List[Location]:
        return [loc for loc in self.__nodes.values() if loc.is_important()]
    
    def get_id_loc_mapping(self) -> Dict[str, str]:
        return self.__nodes

    def get_loc(self, id : str)-> Location:
        return self.__nodes[id]

    def get_loc_by_name(self, name : str) -> Location:
        return self.__nodes[self.get_imp_loc_id_mapping()[name]]

    def __heuristic(self, from_loc : Location, to_loc : Location) -> int:
        return geodesic(from_loc.get_coordinate(), to_loc.get_coordinate()).meters

    def shortest_path(self, from_loc : str, to_loc : str) -> List[List[int]]:
        goal = self.get_loc_by_name(to_loc)
        
        node : Location = self.get_loc_by_name(from_loc)
        previous = {node.get_id() : None}
        
        frontier = PriorityQueue()
        frontier.put((0, node))
        reached = {node.get_id() : 0}
        while not frontier.empty():
            nodep = frontier.get()
            print(type(nodep))
            node = nodep[1]
            if node == goal:
                break
            for path in node.get_neighbouring_path():
                s = path.get_end_loc()
                path_cost_to_s = path.get_distance() + reached[node.get_id()]
                if s.get_id() not in reached or path_cost_to_s < reached[s.get_id()]:
                    reached[s.get_id()] = path_cost_to_s
                    frontier.put((self.__heuristic(s, goal) + path_cost_to_s, s))
                    previous[s.get_id()] = node

        if node == goal:
            path_coordinate = []
            n = goal
            while n != None:
                path_coordinate.insert(0, n.get_coordinate())
                n = previous[n.get_id()]
            return path_coordinate
        else:
            return None

    
    def from_curr_shortest_path(self, coor, to_loc):
        pass


# main.py
from typing import Optional
from typing import Tuple

import matplotlib.pyplot as plt

def main():
    # Initialize Map
    city_map = Map()

    # Create Locations
    loc_a = Location(id="A", name="Alpha", latitude=40.7128, longitude=-74.0060, is_important=True)      # New York
    loc_b = Location(id="B", name="Beta", latitude=34.0522, longitude=-118.2437, is_important=True)     # Los Angeles
    loc_c = Location(id="C", name="Gamma", latitude=41.8781, longitude=-87.6298, is_important=True)     # Chicago
    loc_d = Location(id="D", name="Delta", latitude=29.7604, longitude=-95.3698, is_important=True)     # Houston
    loc_e = Location(id="E", name="Epsilon", latitude=33.4484, longitude=-112.0740, is_important=True)  # Phoenix

    # Add Locations to Map
    city_map.add_loc(loc_a)
    city_map.add_loc(loc_b)
    city_map.add_loc(loc_c)
    city_map.add_loc(loc_d)
    city_map.add_loc(loc_e)

    # Create Paths (Distances in kilometers for simplicity)
    # New York to Chicago
    loc_a.add_neighbouring_path(to_loc=loc_c, distance=1145)
    loc_c.add_neighbouring_path(to_loc=loc_a, distance=1145)

    # Chicago to Houston
    loc_c.add_neighbouring_path(to_loc=loc_d, distance=1515)
    loc_d.add_neighbouring_path(to_loc=loc_c, distance=1515)

    # Houston to Phoenix
    loc_d.add_neighbouring_path(to_loc=loc_e, distance=1890)
    loc_e.add_neighbouring_path(to_loc=loc_d, distance=1890)

    # Phoenix to Los Angeles
    loc_e.add_neighbouring_path(to_loc=loc_b, distance=575)
    loc_b.add_neighbouring_path(to_loc=loc_e, distance=575)

    # New York to Houston
    loc_a.add_neighbouring_path(to_loc=loc_d, distance=1627)
    loc_d.add_neighbouring_path(to_loc=loc_a, distance=1627)

    # Test Shortest Path
    start_location = "Alpha"  # New York
    end_location = "Beta"     # Los Angeles

    print(f"Finding shortest path from {start_location} to {end_location}...")
    path = city_map.shortest_path(from_loc=start_location, to_loc=end_location)

    if path:
        print("Shortest path coordinates:")
        for coord in path:
            print(coord)
    else:
        print("No path found.")

    # Visualization
    visualize_map(city_map, path, start_location, end_location)

def visualize_map(city_map: Map, path: Optional[List[Tuple[float, float]]], start_name: str, end_name: str):
    # Create a plot
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # Plot all paths
    for loc in city_map.get_all_loc():
        y_start, x_start  = loc.get_longitude(), loc.get_latitude()
        for path_i in loc.get_neighbouring_path():
            neighbor = path_i.get_end_loc()
            y_end, x_end = neighbor.get_longitude(), neighbor.get_latitude()
            plt.plot([x_start, x_end], [y_start, y_end], 'lightgray', linewidth=1, zorder=1)

    # Plot all locations
    for loc in city_map.get_all_loc():
        y, x = loc.get_longitude(), loc.get_latitude()
        print(x, y)
        if loc.get_name() == start_name:
            plt.scatter(x, y, color='green', s=100, zorder=2, label='Start')
        elif loc.get_name() == end_name:
            plt.scatter(x, y, color='red', s=100, zorder=2, label='End')
        else:
            plt.scatter(x, y, color='blue', s=50, zorder=2)
        plt.text(x + 0.1, y + 0.1, loc.get_name(), fontsize=9, zorder=3)

    # Highlight the shortest path
    if path:
        path_lons = [coord[1] for coord in path]  # Longitude
        path_lats = [coord[0] for coord in path]  # Latitude
        plt.plot(path_lats, path_lons, color='orange', linewidth=3, label='Shortest Path', zorder=4)

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
