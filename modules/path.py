from location import Location

class Path:
    def __init__(self, start_node : Location, end_node : Location, weight : int):
        self.__start_node = start_node
        self.__end_node = end_node
        self.__weight = weight

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
