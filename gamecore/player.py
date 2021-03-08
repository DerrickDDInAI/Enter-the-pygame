"""
Local modules that defines the player and non-player characters.
"""

# =====================================================================
# Import
# =====================================================================

# Import internal modules
import math
from typing import List, Set, Dict, TypedDict, Tuple, Optional


# =====================================================================
# Classes
# =====================================================================

class Player:
    """
    Player is represented by a circle object.
    At the initialization, it has 9 attributes:
    * name: player's name
    * x_px: player's pixel position in the x direction (at the circle center)
    * y_px: player's pixel position in the y direction (at the circle center)
    * size_px: player's circle radius in pixel
    * mass: player's mass
    * color: player's circle color
    * speed: player's speed
    * angle: player's direction
    * elasticity: player's elasticity.

    """

    def __init__(
        self,
        name: str,
        xy_position_px: Tuple[float],
        size_px: int = 50,
        mass: int = 1,
        color: Tuple[int] = (0, 0, 255)  # RGB color code for blue
    ) -> None:
        """
        Function to create an instance of Player class.
        Player instance is created with no velocity (speed and angle);
        and an elasticity to determine the level of elastic collision 
        between him and another object. 
        """
        self.name: str = name
        self.x_px: float
        self.y_px: float
        self.x_px, self.y_px = xy_position_px
        self.size_px: int = size_px
        self.mass: int = mass
        self.color: Tuple[int] = color

        self.speed: float = 0.0  # player starts with no speed
        self.angle: float = 0.0  # player has no direction yet
        self.elasticity: float = 0.9

    def __repr__(self) -> str:
        """
        Function to print the Player instance in the specified format.
        """
        return f"{self.name}"

    def move(self) -> None:
        """
        Function to update the player's position due to its speed and angle.
        """
        self.x_px += math.sin(self.angle) * self.speed
        self.y_px -= math.cos(self.angle) * self.speed


class AIBots(Player):
    """
    AIBots is a child class of Player class. 
    At the initialization, it inherites the 9 attributes from Player.
    """

    def __init__(
        self,
        name: str,
        xy_position_px: Tuple[float],
        size_px: int = 50,
        mass: int = 1,
        color: Tuple[int] = (255, 0, 0)  # RGB color code for red
    ) -> None:
        """
        Function to create an instance of AIBots class.
        """

        super().__init__(name, xy_position_px, size_px, mass, color)


class Obstacle(Player):
    """
    Obstacle is a child class of Player class. 
    At the initialization, it inherites the 9 attributes from Player.
    """

    def __init__(
        self,
        name: str,
        xy_position_px: Tuple[float],
        size_px: int = 50,
        mass: int = 1,
        color: Tuple[int] = (128, 128, 128)  # RGB color code for grey
    ) -> None:
        """
        Function to create an instance of Obstacle class.
        """

        super().__init__(name, xy_position_px, size_px, mass, color)


class Gorilla:
    """
    Gorilla is a non-player character.
    It is represented by an image surface.
    At the initialization, it has 5 attributes:
    * image: gorilla image
    * image_flip: gorilla image flipped horizontally, by default: None
    * x_px: gorilla's pixel position in the x direction (at the left of the image surface)
    * y_px: gorilla's pixel position in the y direction (at the top of the image surface)
    * dialogues: gorilla lines of dialogue in the story script.
    """

    def __init__(
        self,
        xy_position_px: Tuple[float]
    ) -> None:
        """
        Function to create an instance of Gorilla class.
        """
        self.x_px: float
        self.y_px: float
        self.x_px, self.y_px = xy_position_px
        self.image = None
        self.image_flip = None  # will contain the horizontally flipped image of the gorilla

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
            "What I can tell you is to train yourself!",  # 13
            "..." # 14

            # "Waiiitt come back!"
            # " What does that mean? Train myself? In what? And for what?"
            # "What a very strange gorilla... Well, let's play, maybe I'll find more information.
        ]
