from typing import Dict, List
from location import Location
from geopy.distance import geodesic


class Map: 
    def __init__(self):
        self.__nodes : Dict[str : Location] = {}
    
    def add_loc(self, loc : Location):
        self.__nodes[loc.get_id()] = loc
    
    def del_loc(self, id : str):
        del self.__nodes[id]
    
    def get_imp_loc_id_mapping(self) -> Dict[str : str]:
        loc_id = {}
        important_loc = self.get_important_loc()
        for loc in important_loc:
            loc_id[loc.get_name()] = loc.get_id()
        return loc_id
    
    def get_all_loc(self) -> List[Location]:
        return self.__nodes.copy()
    
    def get_important_loc(self) -> List[Location]:
        return [loc for loc in self.__nodes if loc.is_important()]
    
    def get_loc_id_mapping(self) -> Dict[str : str]:
        return self.__nodes

    def __heuristic(from_loc : Location, to_loc : Location) -> int:
        return 

    def shortest_path(self, from_loc : str, to_loc : str) -> List[List[int]]:
        # A star
        pass
    
    def from_curr_shortest_path(self, coor, to_loc):
        pass