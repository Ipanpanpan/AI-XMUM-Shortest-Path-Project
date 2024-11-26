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

    def add_path(self, id1 : str, id2 : str, distance : float):
        loc1 : Location = self.__nodes[id1]
        loc2 : Location = self.__nodes[id2]
        loc1.add_neighbouring_path(loc2, distance)
        loc2.add_neighbouring_path(loc1, distance)

    
    def get_imp_loc_id_mapping(self) -> Dict[str, str]:
        loc_id = {}
        important_loc = self.get_important_loc()
        for loc in important_loc:
            loc_id[loc.get_name()] = loc.get_id()
        return loc_id
    
    def get_all_loc(self) -> List[Location]:
        return list(self.__nodes.values())
    
    def get_all_loc_id(self) -> List[str]:
        return list(self.__nodes.keys())

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
    
    def __a_star(self, initial : Location, goal : Location) -> List[List[int]]:
        
        node : Location = initial
        previous = {node.get_id() : None}
        
        frontier = PriorityQueue()
        frontier.put((0, node))
        reached = {node.get_id() : 0}
        while not frontier.empty():
            nodep = frontier.get()
            node = nodep[1]
            if node == goal:
                return previous, reached[goal.get_id()]
            for path in node.get_neighbouring_path():
                child = path.get_end_loc()
                path_cost_to_child = path.get_distance() + reached[node.get_id()]
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.put((self.__heuristic(child, goal) + path_cost_to_child, child)) # f(n) = g(n) + h(n)
                    previous[child.get_id()] = node

        return None

    def __greedy(self, initial : Location, goal : Location) -> List[List[int]]:
        
        node : Location = initial
        previous = {node.get_id() : None}
        
        frontier = PriorityQueue()
        frontier.put((0, node))
        reached = {node.get_id() : 0}
        while not frontier.empty():
            node = frontier.get()[1]
            
            if node == goal:
                return previous, reached[goal.get_id()]
            for path in node.get_neighbouring_path():
                child = path.get_end_loc()
                path_cost_to_child = path.get_distance() + reached[node.get_id()]
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.put((self.__heuristic(child, goal), child)) # f(n) =  h(n)
                    previous[child.get_id()] = node

        return None


    def __uniform(self, initial : Location, goal : Location) -> List[List[int]]:
        
        node : Location = initial
        previous = {node.get_id() : None}
        
        frontier = PriorityQueue()
        frontier.put((0, node))
        reached = {node.get_id() : 0}
        while not frontier.empty():
            node = frontier.get()[1]
            
            if node == goal:
                return previous, reached[goal.get_id()]
            for path in node.get_neighbouring_path():
                child = path.get_end_loc()
                path_cost_to_child = path.get_distance() + reached[node.get_id()]
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.put((path_cost_to_child, child)) # f(n) =  h(n)
                    previous[child.get_id()] = node

        return None
    
    def __dfs(self, initial : Location, goal : Location) -> List[List[int]]:
              
        reached = {initial.get_id() : 0}
        previous = {initial.get_id() : None}

        node : Location = initial

        frontier = [node]

        while frontier:
            node = frontier.pop()
            
            if node == goal:
                return previous, reached[goal.get_id()]
            for path in node.get_neighbouring_path():
                child = path.get_end_loc() #child
                path_cost_to_child = path.get_distance() + reached[node.get_id()]
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.append(child) # f(n) =  -depth
                    previous[child.get_id()] = node

        return None


    def __bfs(self, initial : Location, goal : Location) -> List[List[int]]:
              
        reached = {initial.get_id() : 0}
        previous = {initial.get_id() : None}

        node : Location = initial

        frontier = [node]

        while frontier:
            node = frontier.pop(0)
            
            if node == goal:
                return previous, reached[goal.get_id()]
            for path in node.get_neighbouring_path():
                child = path.get_end_loc() #child
                path_cost_to_child = path.get_distance() + reached[node.get_id()]
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.append(child) # f(n) =  -depth
                    previous[child.get_id()] = node

        return None

    def shortest_path(self, from_loc : str, to_loc : str, search_algorithm = "a star") -> List[List[int]]:
        goal = self.get_loc_by_name(to_loc)
        initial = self.get_loc_by_name(from_loc)
        
        if search_algorithm.lower() in ["a star", "a*"]:
            previous, distance = self.__a_star(initial, goal)
        elif search_algorithm.lower() == "greedy":
            previous, distance = self.__greedy(initial, goal)
        elif search_algorithm.lower() in ["uniform", "uni"]:
            previous, distance = self.__uniform(initial, goal)
        elif search_algorithm.lower() in ["dfs", "depth first search", "depth first"]:
            previous, distance = self.__dfs(initial, goal)

        elif search_algorithm.lower() in ["bfs", "breadth first search", "breadth first"]:
            previous, distance = self.__bfs(initial, goal)

        if previous is not None:
            path_coordinate = []
            n = goal
            while n != None:
                path_coordinate.insert(0, n.get_coordinate())
                n = previous[n.get_id()]
            return path_coordinate, distance
        else:
            return None
    
    def from_curr_shortest_path(self, coor, to_loc):
        pass


# main.py
from typing import Optional
from typing import Tuple

import matplotlib.pyplot as plt

import random

def main():
    # Initialize Map
    city_map = Map()
    random.seed(0)
    for i in range(100):
        x, y = random.uniform(0, 10), random.uniform(0, 10)
        loc_i : Location = Location(id = str(i), name = str(i), latitude= x, longitude= y, is_important= True)
        city_map.add_loc(loc_i)
        n_neighbour = random.randint(1, 3)
        for j in range(n_neighbour):
            loc2 = random.choice(city_map.get_all_loc())
            # dis = (sum((k_1 - k_2) ** 2 for k_1, k_2 in 
            #            zip(loc_i.get_coordinate(), loc2.get_coordinate()))) ** (1/2)
            dis = geodesic(loc_i.get_coordinate(), loc2.get_coordinate()).meters
            city_map.add_path(loc_i.get_id(), loc2.get_id(), dis)
        

    # Test Shortest Path
    start_location = "1"  # New York
    end_location = "99"     # Los Angeles

    print(f"Finding shortest path from {start_location} to {end_location}...")
    path, distance = city_map.shortest_path(from_loc=start_location, to_loc=end_location, search_algorithm= "a*")

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
            y_start, x_start  = loc.get_longitude(), loc.get_latitude()
            for path_i in loc.get_neighbouring_path():
                neighbor = path_i.get_end_loc()
                y_end, x_end = neighbor.get_longitude(), neighbor.get_latitude()
                plt.plot([x_start, x_end], [y_start, y_end], 'lightgray', linewidth=1, zorder=1)

    # Plot all locations
    for loc in city_map.get_all_loc():
        y, x = loc.get_longitude(), loc.get_latitude()
        if loc.get_name() == start_name:
            plt.scatter(x, y, color='green', s=100, zorder=2, label='Start')
        elif loc.get_name() == end_name:
            plt.scatter(x, y, color='red', s=100, zorder=2, label='End')
        else:
            plt.scatter(x, y, color='blue', s=50, zorder=2)
        if text_on:
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
