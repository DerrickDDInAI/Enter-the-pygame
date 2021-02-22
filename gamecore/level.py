"""
Local modules that defines the Level class
"""
#=====================================================================
# Import
#=====================================================================

## Import internal modules
from typing import List, Set, Dict, TypedDict, Tuple, Optional


#=====================================================================
# Classes
#=====================================================================

class Level:
    """
    Level has 4 attributes: name, level_number, level_type, bg_surface_path 
    * name: name of the level
    * level_number: level number
    * level_type: type of the level; there are 2 types of level in this game: "slide" or "game_level"
    * bg_surface_path: filepath of the background surface image that we'll use to load
    """

    # Class attributes
    count_created_levels: int = 0
    levels_list: List = []
    
    def __init__(
        self,
        name: str = None,
        level_type: str = "game_level",
        bg_surface_path: str = None
    ):
        """
        Function to create an instance of Level class
        By default:
        * name is "level_1", then "level_2" if no name is provided
        * level_type is "game_level"
        * bg_surface is None
        """
        Level.count_created_levels += 1
        self.level_number = Level.count_created_levels
        if name is None:
            self.name = f"Level_{self.level_number}"
        else:
            self.name = name
        
        self.level_type = level_type
        self.bg_surface_path = bg_surface_path

        Level.levels_list.append(self)

    def __repr__(self):
        """
        In order to print the Level instance in the specified format
        """
        return f'Level {self.level_number}: "{self.name}" ({self.level_type})'


#============================================================
# Main functions
#============================================================

def main():
    level_1 = Level("Title", "slide")
    level_2 = Level("Terminal")
    print(level_1)
    print(level_2)


#============================================================
# Run
#============================================================

## if you directly run this program, main() fct will create 2 player instances and print them
if __name__ == '__main__':
    main()