from typing import Dict, List, Tuple, Optional, Union
from location import Location, Path
from geopy.distance import geodesic
from queue import PriorityQueue
import numpy as np


class Map: 
    """this class represents a map or a graph of locations and paths between them"""
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

    def get_all_search_algorithm(self) -> List[str]:
        return ["a star", "greedy", "uniform", "dfs", "bfs", "bidirectional heuristic", "iterative deepening a star", "iterative deepening DFS"]
    
    def get_imp_loc_id_mapping(self) -> Dict[str, str]:
        """returns a dictionary mapping the name of important locations to their ids"""
        loc_id = {}
        important_loc = self.get_important_loc()
        for loc in important_loc:
            loc_id[loc.get_name().strip().lower()] = loc.get_id()
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
        return self.__nodes[self.get_imp_loc_id_mapping()[name.strip().lower()]]

    def __heuristic(self, from_loc : Location, to_loc : Location) -> int:
        return geodesic(from_loc.get_coordinate(), to_loc.get_coordinate()).meters
    
    def __a_star(self, initial : Location, goal : Location) -> Tuple[Dict[int, Optional[Location]], int]:
        """this function uses A* Search to find the shortest path between two locations"""
        node : Location = initial
        previous = {node.get_id() : None}
        
        frontier = PriorityQueue()
        frontier.put((0.0, node))
        reached = {node.get_id() : 0}
        
        #Start search
        while not frontier.empty():
            node = frontier.get()[1] #Get the node with the lowest f(n)
            if node == goal: #Goal reached
                return previous, reached[goal.get_id()]
            #Expand node
            for path in node.get_neighbouring_path():
                
                child = path.get_end_loc() 
                path_cost_to_child = path.get_distance() + reached[node.get_id()] #g(n)

                #add child to frontier
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    f_score = path_cost_to_child + self.__heuristic(child, goal)  # f(n) = g(n) + h(n)
                    frontier.put((f_score, child))
                    previous[child.get_id()] = node
                    try:
                        print("previous:", [(self.__nodes[id1] , loc.get_name())for id1, loc in previous.items()])
                    except:
                        pass

        raise PathNotFoundException("No path found from initial to goal.")

    def __greedy(self, initial : Location, goal : Location) -> List[List[int]]:
        """this function uses Greedy Search to find the shortest path between two locations"""
        node : Location = initial
        previous = {node.get_id() : None}
        
        frontier = PriorityQueue()
        frontier.put((0, node))
        reached = {node.get_id() : 0}
        
        #Start search
        while not frontier.empty():
            node = frontier.get()[1]

            if node == goal: #Goal reached
                return previous, reached[goal.get_id()]
            
            #Expand node
            for path in node.get_neighbouring_path():
                child = path.get_end_loc()
                path_cost_to_child = path.get_distance() + reached[node.get_id()]

                #add child to frontier
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.put((self.__heuristic(child, goal), child)) # f(n) =  h(n)
                    previous[child.get_id()] = node

        raise PathNotFoundException("No path found from initial to goal.")


    def __uniform(self, initial : Location, goal : Location) -> List[List[int]]:
        """this function uses Uniform Cost Search to find the shortest path between two locations"""

        node : Location = initial
        previous = {node.get_id() : None}
        
        frontier = PriorityQueue()
        frontier.put((0, node))
        reached = {node.get_id() : 0}

        #Start search
        while not frontier.empty():
            # print_queue(frontier)
            node = frontier.get()[1]
            
            if node == goal: #Goal reached
                return previous, reached[goal.get_id()]
            #Expand node
            for path in node.get_neighbouring_path():
                
                child = path.get_end_loc()
                path_cost_to_child = path.get_distance() + reached[node.get_id()]

                #add child to frontier
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.put((path_cost_to_child, child)) # f(n) =  g(n)
                    previous[child.get_id()] = node
        raise PathNotFoundException("No path found from initial to goal.")
    
    def __dfs(self, initial : Location, goal : Location) -> List[List[int]]:
        """this function uses Depth-First Search to find the shortest path between two locations"""
        reached = {initial.get_id() : 0}
        previous = {initial.get_id() : None}

        node : Location = initial

        #Initialize frontier as a stack
        frontier = [node]

        #Start search
        while frontier:
            node = frontier.pop()
            
            #Goal reached
            if node == goal:
                return previous, reached[goal.get_id()]
            
            #Expand node
            for path in node.get_neighbouring_path():
                child = path.get_end_loc() #child
                path_cost_to_child = path.get_distance() + reached[node.get_id()]

                #add child to frontier
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.append(child) 
                    previous[child.get_id()] = node

        raise PathNotFoundException("No path found from initial to goal.")


    def __bfs(self, initial : Location, goal : Location) -> List[List[int]]:
        """this function uses Breadth-First Search to find the shortest path between two locations"""
        reached = {initial.get_id() : 0}
        previous = {initial.get_id() : None}

        node : Location = initial

        #Initialize frontier as a queue
        frontier = [node]

        while frontier:
            node = frontier.pop(0)
            
            #Goal reached
            if node == goal:
                return previous, reached[goal.get_id()]
            
            #Expand node
            for path in node.get_neighbouring_path():
                child = path.get_end_loc() #child
                path_cost_to_child = path.get_distance() + reached[node.get_id()]

                #add child to frontier
                if child.get_id() not in reached or path_cost_to_child < reached[child.get_id()]:
                    reached[child.get_id()] = path_cost_to_child
                    frontier.append(child) # f(n) =  -depth
                    previous[child.get_id()] = node

        raise PathNotFoundException("No path found from initial to goal.")

    def __bidirectional_heuristic(self, initial : Location, goal : Location) -> List[List[int]]:
        """this function uses Bidirectional Heuristic Search to find the shortest path between two locations"""
        node_f : Location = initial
        node_b : Location = goal

        frontier_f = PriorityQueue()
        frontier_b = PriorityQueue()

        frontier_f.put((0.0, node_f))
        frontier_b.put((0.0, node_b))

        reached_f = {initial.get_id() : 0}
        previous_f = {initial.get_id() : None}

        reached_b = {goal.get_id() : 0}
        previous_b = {goal.get_id() : None}

        expanded_f = []
        expanded_b = []

        solution = None

        while not frontier_f.empty() and not frontier_b.empty():
            if frontier_f.queue[0][0] < frontier_b.queue[0][0]:
                #Expand node at f
                node_f = frontier_f.get()[1]
                expanded_f.append(node_f.get_id())

                #Check if node_f has been expanded by backward search
                if node_f.get_id() in expanded_b:
                    solution = node_f
                    break

                #Expand node at f
                for path in node_f.get_neighbouring_path():
                    child = path.get_end_loc()
                    path_cost_to_child = path.get_distance() + reached_f[node_f.get_id()]
                    if child.get_id() not in reached_f or path_cost_to_child < reached_f[child.get_id()]:
                        reached_f[child.get_id()] = path_cost_to_child
                        f_score = max(2 * path_cost_to_child, path_cost_to_child + self.__heuristic(child, goal))  # f(n) = g(n) + h(n)
                        frontier_f.put((f_score, child))
                        previous_f[child.get_id()] = node_f
            else:
                #Expand node at b
                node_b = frontier_b.get()[1]
                expanded_b.append(node_b.get_id())

                #Check if node_b has been expanded by forward search
                if node_b.get_id() in expanded_f:
                    solution = node_b
                    break
                
                #Expand node at b
                for path in node_b.get_neighbouring_path():
                    child = path.get_end_loc()
                    path_cost_to_child = path.get_distance() + reached_b[node_b.get_id()]
                    if child.get_id() not in reached_b or path_cost_to_child < reached_b[child.get_id()]:
                        reached_b[child.get_id()] = path_cost_to_child
                        f_score = max(2 * path_cost_to_child, path_cost_to_child + self.__heuristic(child, initial))
                        frontier_b.put((f_score, child))
                        previous_b[child.get_id()] = node_b
        
        # Construct the path if a solution is found
        if solution is not None:
            path = []
            n = solution
            while n is not None:
                path.insert(0, n.get_coordinate())
                n = previous_f[n.get_id()]
            n = solution
            while n is not None:
                path.append(n.get_coordinate())
                n = previous_b[n.get_id()]
            return path, reached_f[solution.get_id()] + reached_b[solution.get_id()]
        else:
            raise PathNotFoundException("No path found from initial to goal.")

    
    def __iterative_deepening_search(self, initial: Location, goal: Location) -> Tuple[List[List[int]], int]:
        """
        this function defines Iterative Deepening Depth-First Search to find the shortest path between two locations
        by recursively exploring paths up to a depth limit and increasing it iteratively
        """    
        def dfs_with_depth_limit(node: Location, depth: int, visited: set) -> Tuple[Optional[List[Location]], Optional[int]]:
            
            if node == goal:
                return [node], 0
            if depth == 0:
                return None, None
            if node in visited:
                return None, None
            
            visited.add(node)

            # Explore all neighboring paths from current node
            for path in node.get_neighbouring_path():
                child = path.get_end_loc()
                path_cost = path.get_distance()
                # Recursively perform DFS on the child node with reduced depth
                result, cost = dfs_with_depth_limit(child, depth - 1, visited)
                
                # Append node if valid path is found
                if result:
                        return ([node] + result, path_cost + cost)
                
            visited.remove(node)
            return None, None
        
        depth_limit = len(self.__nodes)
        depth = 0

        # Start the search
        while depth <= depth_limit:
            visited = set()
            result, total_cost = dfs_with_depth_limit(initial, depth, visited)
            
            if result:
                path_coordinates = [[loc.get_latitude(), loc.get_longitude()] for loc in result]
                return path_coordinates, total_cost
            depth += 1 # Increment the depth limit for the next iteration

        raise PathNotFoundException("No path found from initial to goal.")



    def __iterative_deepening_a_star (self, initial : Location, goal : Location) -> Tuple[List[List[int]], int]:
        """this function defines Iterative Deepening A* Search to find the shortest path between two locations"""

        # threshold limited search
        def dfs(current: Location, g: float, threshold: float, path: List[Location], visited: set) -> Tuple[Optional[float], Optional[List[Location]]]:
            f = g + self.__heuristic(current, goal)

            # If f(n) exceeds the threshold, return the value
            if f > threshold:
                return f, None
            if current == goal:
                return g, path[:]
            
            
            min_threshold = float('inf')

            # Explore all neighboring paths from current node
            for neighbor_path in current.get_neighbouring_path():
                neighbor = neighbor_path.get_end_loc()
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                path.append(neighbor)
                cost_to_neighbor = neighbor_path.get_distance()

                # Recursively perform DFS on the child node
                result, solution_path = dfs(neighbor, g + cost_to_neighbor, threshold, path, visited)
                if solution_path is not None:
                    return result, solution_path
                
                min_threshold = min(min_threshold, result)
                path.pop()
                visited.remove(neighbor)

            return min_threshold, None
        
        threshold = self.__heuristic(initial, goal)
        path = [initial]

        # Start the search
        while True:
            visited = {initial}
            # Perform DFS with threshold
            result, solution_path = dfs(initial, 0, threshold, path, visited)
            if solution_path is not None:
                return [[loc.get_coordinate() for loc in solution_path], result]
            if result == float('inf'):
                raise PathNotFoundException("No path found from initial to goal.")
            threshold = result
                           
        
    def shortest_path(self, from_loc : Union[str, list], to_loc : str, search_algorithm = "a star") -> List[List[int]]:
        """this function finds the shortest path between two locations using the specified search algorithm"""

        # set the initial and goal locations from the input
        if isinstance(from_loc, list) and len(from_loc) == 2:
            initial = find_nearest_location(from_loc, self)
        elif isinstance(from_loc, str):
            initial = self.get_loc_by_name(from_loc)
        else:
            raise ValueError("Invalid from_loc.")
        
        goal = self.get_loc_by_name(to_loc)


        # Call the appropriate search algorithm
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
        elif search_algorithm.lower() in ["bidir", "bidirectional heuristic", "bidirectional"]:
            previous, distance = self.__bidirectional_heuristic(initial, goal)
        elif search_algorithm.lower() in ["id a star", "ida*", "iterative deepening a*", "iterative deepening a star", "deepening a*", "deepening a star"]:
            previous, distance = self.__iterative_deepening_a_star(initial, goal)
        elif search_algorithm.lower() in ["iterative deepening", "id", "deepening", "iterative deepening dfs"]:
            previous, distance = self.__iterative_deepening_search(initial, goal)
        else:
            raise ValueError("Invalid search algorithm.")
        
        #if the path already constructed, return it
        if isinstance(previous, list):
            return previous, distance


        # Construct the path from the previous dictionary
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

def find_nearest_location(coord, map, locs_coor = None):
    """this function finds the nearest location to the given coordinate"""

    # Get the coordinates of all locations if not provided
    if not isinstance(locs_coor, type(np.array([]))):
        locs_coor = np.array([[loc.get_latitude(), loc.get_longitude()] for loc in map.get_all_loc()])
    
    coord = np.array(coord)
    
    #calculate distances
    distances = np.linalg.norm(locs_coor - coord, axis=1) 
    
    #find the index of the minimum distance
    index = np.argmin(distances)
    
    return map.get_all_loc()[index]

class PathNotFoundException(Exception):
    pass

