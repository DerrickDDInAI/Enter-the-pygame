#=====================================================================
# Classes
#=====================================================================

class Player:
    """
    Player is a circle.
    It has 2 attributes: name, xxx
    * name: xxx
    * xxx: xxx
    
    And Player class has 2 class attributes: count_created_players, players_list
    * count_created_players: int starting at 0, to count the number of players created
    * players_list: empty list to store the players
    """

    # class attributes
    count_created_players:int = 0
    players_list: list = []
    
    def __init__(
        self,
        radius: int,
        xy_pos: tuple,
        name: str = None,
        color: tuple = (0,0,255), # RGB color code for blue
        boost: float = 5.0
        # self.speed_x: float = 
        # self.speed_y: float = 
    ) -> None:
        """
        Function to create an instance of Player class
        By default:
        * name is "player_1", then "player_2" if no name is provided
        * boost is 5.0 
          (when player uses boost: boost is set to 0 and has to wait 5.0 seconds to use it again)
        """
        Player.count_created_players += 1
        self.radius = radius
        self.x: int
        self.y: int
        self.x, self.y = xy_pos
        
        if name is None:
            self.name = f"player_{Player.count_created_players}"
        else:
            self.name = name
        
        self.color = color
        self.boost = boost


        Player.players_list.append(self)

    def __repr__(self):
        """
        In order to print the Player instance in the specified format
        """
        return f"{self.name}"

class AIBots(Player):
    """
    AIBots is a child class of Player class. 
    It has 2 attributes: name, xxx
    * name: xxx
    * xxx: xxx
    
    And AIBots class has 2 class attributes: count_created_aibots, aibots_list
    * count_created_aibots: int starting at 0, to count the number of aibots created
    * aibots_list: empty list to store the aibots
    """

    # class attributes
    count_created_aibots: int = 0
    aibots_list: list = []
    
    def __init__(
        self,
        radius: int,
        xy_pos: tuple,
        name: str = None,
        color: tuple = (255,0,0), # RGB color code for red
        boost: float = 5.0
        # self.speed_x: float = 
        # self.speed_y: float = 
    ) -> None:
        """
        Function to create an instance of AIBots class
        By default:
        * name is "aibots_1", then "aibots_2" if no name is provided
        * boost is 5.0 
          (when player uses boost: boost is set to 0 and has to wait 5.0 seconds to use it again)
        """
        AIBots.count_created_aibots += 1
        if name is None:
            self.name = f"aibots_{AIBots.count_created_aibots}"
        else:
            self.name = name
        super().__init__(radius, xy_pos, self.name, color, boost)

        AIBots.aibots_list.append(self)


#============================================================
# Main functions
#============================================================

def main():
    player_1 = Player(20, (1,1),'Yoyo', (255,0,0))
    player_2 = Player(20, (2,2))
    aibots_1 = AIBots(20, (3,3),"I-Bot")
    aibots_2 = AIBots(20, (4,4))
    print(f"{player_1} vs {aibots_1}")
    print(f"{player_2} vs {aibots_2}")


#============================================================
# Run
#============================================================

## if you directly run this program, main() fct will create 2 player instances and print them
if __name__ == '__main__':
    main()