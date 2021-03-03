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
        # self.speed_x: float = 
        # self.speed_y: float = 


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
    ) -> None:
        """
        Function to create an instance of AIBots class
        By default:
        * name is "aibots_1", then "aibots_2" if no name is provided
        * boost is 5.0 
          (when player uses boost: boost is set to 0 and has to wait 5.0 seconds to use it again)
        """
        AIBots.count_created_aibots += 1
        self.radius = radius
        self.x: int
        self.y: int
        self.x, self.y = xy_pos

        if name is None:
            self.name = f"aibots_{AIBots.count_created_aibots}"
        else:
            self.name = name
        # super().__init__(radius, xy_pos, self.name, color, boost)

        self.color = color
        self.boost = boost
        # self.speed_x: float = 
        # self.speed_y: float = 

        AIBots.aibots_list.append(self)


class Gorilla:
    """
    Gorilla class
    """
    def __init__(
        self,
        image_path: str,
        xy_pos: tuple
    ) -> None:
        """
        Function to create an instance of Gorilla class
        """
        self.image_path = image_path
        self.x: int
        self.y: int
        self.x, self.y = xy_pos
    
    def talk(self, line_nb: int):
        """
        Function to make the Gorilla talk

        My lines:
        1. "Let's dive into the game!"
        4. "Whaat! Wait... who are you?"
        5. "Another dimension? You created your designer?"
           "You waited for 29 years that he draws you like this ?!
           "Sorry to say but you're not exactly a picasso!"
           "Wait, that's not what is important. Why are you here?"
        8. "A convergence?"
        12. "Waiiitt come back!"
            " What does that mean? Train myself? In what? And for what?"
            "What a very strange gorilla... Well, let's play, maybe I'll find more information.
        """
        lines = [
            "You're wrong.", # 1
            "You're already in the game.", # 2
            "You've always been in the game!", # 3
            "My name is Mastro Gorilla.", # 4
            "I am a being from another dimension.", # 5
            "29 years ago in human time, I created my designer so that he could draw me.", # 6
            "From my dimension, we can see your past, present and all possible futures.", # 7
            "What we... what I saw in the chain of possibilities is a convergence." # 8
            "Something that must never happen!" # 9
            "However, I can't tell you more than that." # 10
            "You're not ready... yet." # 11
            "What I can tell you is to train yourself!"
        ]
        return lines[line_nb]
        


#============================================================
# Main functions
#============================================================

def main():
    player_1 = Player(20, (1,1),'Yoyo', (255,0,0))
    player_2 = Player(20, (2,2))
    aibots_1 = AIBots(20, (3,3),"I-Bot")
    aibots_2 = AIBots(20, (4,4))
    player_3 = Player(20, (5,5)) 
    print(f"{player_1} vs {aibots_1}")
    print(f"{player_2} vs {aibots_2}")
    print(player_3)

#============================================================
# Run
#============================================================

## if you directly run this program, main() fct will create 2 player instances and print them
if __name__ == '__main__':
    main()