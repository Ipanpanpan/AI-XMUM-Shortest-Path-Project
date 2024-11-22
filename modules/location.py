from typing import List, Tuple
from path import Path

class Location:
    def __init__(self, name : str, latitude : int, longitude : int, id : str, is_important : bool):
        self.__name = name
        self.__latitude = latitude
        self.__longitude = longitude
        self.__id = id
        self.__is_important = is_important
        self.__edges : List[Path] = []
    
    def get_name(self) -> str:
        return self.__name
    
    def get_latitude(self) -> int:
        return self.__latitude
    
    def get_longitude(self) -> int:
        return self.__longitude
    
    def get_id(self) -> str:
        return self.__id
    
    def get_neighbouring_path(self) -> List[Path]:
        return self.__edges.copy()
    
    def get_neighbouring_loc(self) -> List["Location"]:
        return [edge.__end_node for edge in self.__edges]

    def get_coordinate(self) -> Tuple[int, int]:
        return (self.get_latitude(), self.get_longitude())
    
    def is_important(self) -> bool:
        return self.__is_important
    
    def set_name(self, name : str):
        self.__name = name

    def set_latitude(self, latitude : int):
        self.__latitude = latitude

    def set_longitude(self, longitude : int):
        self.__longitude = longitude

    def add_neighbouring_path(self, to_loc : "Location", distance : int):
        self.__edges.append(Path(self, to_loc, distance))

