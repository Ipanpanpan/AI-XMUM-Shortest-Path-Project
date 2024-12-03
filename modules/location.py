from typing import List, Tuple

class Location:
    """this class represents a location in the map or a node in the graph"""
    def __init__(self, name : str, latitude : float, longitude : float, id : str, is_important : bool):
        self.__name = name
        self.__latitude = latitude
        self.__longitude = longitude
        self.__id = id
        self.__is_important = is_important
        self.__edges : list[Path] = []
    
    def __eq__(self, other):
        if isinstance(other, Location):
            return self.get_id() == other.get_id()
        return False
    
    def __hash__(self):
        return hash(self.get_id())
    
    def __repr__(self):
        return f"Location(name={self.__name}, id={self.__id})"

    def get_name(self) -> str:
        return self.__name
    
    def get_latitude(self) -> float:
        return self.__latitude
    
    def get_longitude(self) -> float:
        return self.__longitude
    
    def get_coordinate(self) -> Tuple[float, float]:
        return (self.get_latitude(), self.get_longitude())
    
    def get_id(self) -> str:
        return self.__id
    
    def get_neighbouring_path(self) -> List['Path']:
        return self.__edges.copy()
    
    def get_neighbouring_loc(self) -> List["Location"]:
        return [edge.__end_node for edge in self.__edges]
    
    def is_important(self) -> bool:
        return self.__is_important
    
    def set_name(self, name : str):
        self.__name = name

    def set_latitude(self, latitude : int):
        self.__latitude = latitude

    def set_longitude(self, longitude : int):
        self.__longitude = longitude

    def add_neighbouring_path(self, to_loc : "Location", distance : int):
        path = Path(self, to_loc, distance)
        if path not in self.__edges and self != to_loc:
            self.__edges.append(path)
        




class Path:
    """this class represents a path between two locations in the map or an edge in the graph"""

    def __init__(self, start_node : Location, end_node : Location, weight : int):
        self.__start_node = start_node
        self.__end_node = end_node
        self.__weight = weight

    def __eq__(self, other):
        if isinstance(other, Path):
            return (self.__start_node == other.__start_node and
                    self.__end_node == other.__end_node)
    
    def __repr__(self):
        return f"Path(start={self.__start_node.get_name()}, end={self.__end_node.get_name()}, distance={self.__weight})"


    def get_start_loc(self) -> Location:
        return self.__start_node

    def get_end_loc(self) -> Location:
        return self.__end_node
    
    def get_distance(self) -> int:
        return self.__weight
    
    def set_start_loc(self, loc : Location):
        self.__start_node = loc

    def set_end_loc(self, loc : Location):
        self.__end_node = loc

def main():
    loc1 = Location(name="Clock Tower", latitude=1.0, longitude=2.0, id="A", is_important=True)
    loc2 = Location(name="Guard House", latitude=3.0, longitude=4.0, id="B", is_important=False)
    loc3 = Location(name="Clock Tower Duplicate", latitude=1.0, longitude=2.0, id="A", is_important=True)
    
    print(loc1 == loc3)  # True (IDs are the same)
    print(loc1 == loc2)  # False
    print(hash(loc1), hash(loc3), hash(loc2))  # loc1 and loc3 hashes should match
    print(loc1)  # Location(name=Clock Tower, id=A)

if __name__ == "__main__":
    main()