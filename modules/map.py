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



