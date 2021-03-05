# =====================================================================
# Import
# =====================================================================

# Import internal modules
import math
from typing import List, Set, Dict, TypedDict, Tuple, Optional

# Import 3rd party modules


# Import local modules


# =====================================================================
# Classes
# =====================================================================

# from pygame import math
import math


class Player:
    """
    Player is a circle.
    Has velocity, size and mass
    It has 2 attributes: name, xxx
    * name: xxx
    * xxx: xxx

    And Player class has 2 class attributes: count_created_players, players_list
    * count_created_players: int starting at 0, to count the number of players created
    * players_list: empty list to store the players
    """

    # class attributes
    count_created_players: int = 0
    players_list: list = []

    def __init__(
        self,
        xy_position: tuple,
        size=50,
        mass: int = 1,
        name: str = None,
        color: tuple = (0, 0, 255),  # RGB color code for blue
    ) -> None:
        """
        Function to create an instance of Player class
        By default:
        * name is "player_1", then "player_2" if no name is provided
        * boost is 5.0 
          (when player uses boost: boost is set to 0 and has to wait 5.0 seconds to use it again)
        """
        Player.count_created_players += 1
        self.x: int
        self.y: int
        self.x, self.y = xy_position
        self.size = size
        self.thickness = 0
        self.speed = 0  # player starts with no speed
        self.angle = 0
        self.mass = mass
        self.elasticity = 0.9

        if name is None:
            self.name = f"player_{Player.count_created_players}"
        else:
            self.name = name

        self.color: Tuple[int, int, int] = color
        self.boost: float = 5.0

        Player.players_list.append(self)

    def __repr__(self):
        """
        In order to print the Player instance in the specified format
        """
        return f"{self.name}"

    def move(self):
        """
        Function to move the player according to its speed and angle
        """
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed


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
        xy_position: tuple,
        size=50,
        mass: int = 1,
        name: str = None,
        color: tuple = (255, 0, 0),  # RGB color code for red
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
        self.x: int
        self.y: int
        self.x, self.y = xy_position
        self.size = size
        self.thickness = 0
        self.speed = 0  # aibot starts with no speed
        self.angle = 0
        self.mass = mass
        self.elasticity = 0.9

        if name is None:
            self.name = f"aibots_{AIBots.count_created_aibots}"
        else:
            self.name = name
        # super().__init__(radius, xy_pos, self.name, color, boost)

        self.color = color
        self.boost = boost

        AIBots.aibots_list.append(self)


class Obstacle (Player):
    """
    Obstacle is a rectangle.
    """

    # class attributes
    count_created_obstacles: int = 0
    players_list: list = []

    def __init__(
        self,
        xy_position: tuple,
        size=50,
        mass: int = 1,
        name: str = None,
        color: tuple = (128, 128, 128),  # RGB color code for grey
    ) -> None:
        """
        Function to create an instance of Obstacle class
        """
        Obstacle.count_created_obstacles += 1
        self.x: int
        self.y: int
        self.x, self.y = xy_position
        self.size = size
        self.thickness = 0
        self.speed = 0  # player starts with no speed
        self.angle = 0
        self.mass = mass
        self.elasticity = 2

        if name is None:
            self.name = f"obstacle_{Obstacle.count_created_obstacles}"
        else:
            self.name = name

        self.color: Tuple[int, int, int] = color

        Obstacle.players_list.append(self)


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
        self.image = None
        self.image_flip = None  # will contain the horizontally flipped image of the gorilla
        self.x: int
        self.y: int
        self.x, self.y = xy_pos

        """
        My lines:
        0. "Let's dive into the game!"
        3. "Whaat? Who's there?"
        6. "Another dimension? You created your designer?"
           "You waited for 29 years that he draws you like this ?!
           "Sorry to say but you're not exactly a picasso!"
           "Wait, that's not what is important. Why are you here?"
        7. "A convergence?"
        11. "Waiiitt come back!"
            " What does that mean? Train myself? In what? And for what?"
            "What a very strange gorilla... Well, let's play, maybe I'll find more information.
        """
        self.dialogues = [
            # "Let's dive into the game!"
            "You're wrong.",  # 0
            "You're already in the game.",  # 1
            "You've always been in the game!",  # 2

            # "Whaat? Who's there?"
            "...",  # 3
            "My name is Maestro Gorilla.",  # 4
            "I am a being from another dimension.",  # 5
            "29 years ago in human time...",  # 6
            "I created my designer so that he could draw me.",  # 7

            # "Another dimension? You created your designer?"
            # "You waited for 29 years that he draws you like this ?!
            # "Sorry to say but you're not exactly a picasso!"
            # "Wait, that's not what is important. Why are you here?"
            "From my dimension, we can see your past, present and all possible futures.",  # 8
            "What we... what I saw in the chain of possibilities is a convergence.",  # 9

            # "A convergence?"
            "Something that must never happen!",  # 10
            "However, I can't tell you more than that.",  # 11
            "You're not ready... yet.",  # 12
            "What I can tell you is to train yourself!"  # 13

            # "Waiiitt come back!"
            # " What does that mean? Train myself? In what? And for what?"
            # "What a very strange gorilla... Well, let's play, maybe I'll find more information.
        ]

    def move(self):
        pass
# ============================================================
# Main functions
# ============================================================


def main():
    player_1 = Player(20, (1, 1), 'Yoyo', (255, 0, 0))
    player_2 = Player(20, (2, 2))
    aibots_1 = AIBots(20, (3, 3), "I-Bot")
    aibots_2 = AIBots(20, (4, 4))
    player_3 = Player(20, (5, 5))
    print(f"{player_1} vs {aibots_1}")
    print(f"{player_2} vs {aibots_2}")
    print(player_3)

# ============================================================
# Run
# ============================================================


# if you directly run this program, main() fct will create 2 player instances and print them
if __name__ == '__main__':
    main()
