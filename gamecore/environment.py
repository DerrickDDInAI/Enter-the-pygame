"""
Local modules that defines the Environment class
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

class Environment:
    """
    Environment defines the physics and boundaries of the game.
    At the initialization, it has 7 attributes:
    * width_px: environment width in pixel
    * height_px: environment height in pixel
    * color: environment color
    * air_mass: mass of the air to add air resistance
    * elasticity: elasticity of the environment boundaries
    * gravity: gravity direction and magnitude.
    """

    def __init__(self, size_px: Tuple[int], color: Tuple[int] = (255, 255, 255)) -> None:
        self.width_px: int
        self.height_px: int
        self.width_px, self.height_px = size_px
        self.color: Tuple[int] = color
        self.air_mass: float = 0.02
        self.elasticity: float = 0.75
        # math.pi sets gravtity direction pointing downward
        self.gravity: Tuple[float] = (math.pi, 0.01)

    def add_vectors(self, vector_1, vector_2) -> Tuple[float]:
        """
        Function to add 2 vectors.
        A vector has a magnitude and a direction.

        Returns: sum of vector_1 and vector_2
        """
        angle_1: float
        angle_2: float
        magnitude_1: float
        magnitude_2: float

        angle_1, magnitude_1 = vector_1
        angle_2, magnitude_2 = vector_2
        x = math.sin(angle_1) * magnitude_1 + math.sin(angle_2) * magnitude_2
        y = math.cos(angle_1) * magnitude_1 + math.cos(angle_2) * magnitude_2

        angle: float = 0.5 * math.pi - math.atan2(y, x)
        magnitude: float = math.hypot(x, y)

        return (angle, magnitude)

    def add_air_resistance(self, player) -> None:
        """
        Function to make the player (or any of its child instance classes)
        experience air resistance.
        This air resistance slows its speed.
        """
        player.speed *= (player.mass/(player.mass +
                                      self.air_mass)) ** player.size_px

    def accelerate(self, player, vector: Tuple[float]) -> None:
        """
        Function to accelerate (= change speed and/or angle)
        the player (or any of its child instance classes)
        by adding a vector.
        """
        player.angle, player.speed = self.add_vectors(
            (player.angle, player.speed), vector)

    def attraction(self, player_1, player_2) -> Optional[bool]:
        """
        Function to change the velocity (= speed and direction)
        due to gravitational attraction between 2 players
        (or any of its child instance classes)

        Returns: None or True if player.
        """
        # Get the distances in the x direction and in the y direction
        distance_x: float = player_1.x_px - player_2.x_px
        distance_y: float = player_1.y_px - player_2.y_px

        # Compute the distance between the 2 players
        distance: float = math.hypot(distance_x, distance_y)

        # If distance < sum of players' radius, it means collision;
        # No attraction effect anymore
        if distance < player_1.size_px + player_2.size_px:
            return True

        # Use Newton's law of universal gravitation
        theta: float = math.atan2(distance_y, distance_x)
        force: float = 0.1 * player_1.mass * player_2.mass / distance**2
        self.accelerate(player_1, (theta - 0.5 * math.pi, force/player_1.mass))
        self.accelerate(player_2, (theta + 0.5 * math.pi, force/player_2.mass))

    def collide(self, player_1, player_2, apply: bool) -> Optional[bool]:
        """
        Function to check if collision between 2 players
        and if collision and apply is True, make them bounce.

        Returns: None or True if collision.
        """
        # Get the distances in the x direction and in the y direction
        distance_x: float = player_1.x_px - player_2.x_px
        distance_y: float = player_1.y_px - player_2.y_px

        # Compute the distance between the 2 players
        distance: float = math.hypot(distance_x, distance_y)

        # If distance < sum of players' radius, it means collision
        if distance < player_1.size_px + player_2.size_px:
            if apply:
                angle: float = math.atan2(
                    distance_y, distance_x) + 0.5 * math.pi
                total_mass: int = player_1.mass + player_2.mass

                player_1_vector_a = (
                    player_1.angle, player_1.speed * (player_1.mass - player_2.mass) / total_mass)
                player_1_vector_b = (
                    angle, 2 * player_2.speed * player_2.mass / total_mass)
                player_1.angle, player_1.speed = self.add_vectors(
                    player_1_vector_a, player_1_vector_b)

                player_2_vector_a = (
                    player_2.angle, player_2.speed * (player_2.mass - player_1.mass) / total_mass)
                player_2_vector_b = (angle + math.pi, 2 *
                                     player_1.speed * player_1.mass / total_mass)
                player_2.angle, player_2.speed = self.add_vectors(
                    player_2_vector_a, player_2_vector_b)

                elasticity: float = player_1.elasticity * player_2.elasticity
                player_1.speed *= elasticity
                player_2.speed *= elasticity

                # At the time, we detect the collision, the players' circles could possibly have overlapped
                # We correct their positions to remove this overlap
                overlap: float = 0.5 * \
                    (player_1.size_px + player_2.size_px - distance + 1)
                player_1.x_px += math.sin(angle) * overlap
                player_1.y_px -= math.cos(angle) * overlap
                player_2.x_px -= math.sin(angle) * overlap
                player_2.y_px += math.cos(angle) * overlap

            return True

    def bounce(self, player) -> bool:
        """
        Function to check if a player (or any of its child instance classes)
        hits the environment boundary and if so, make it bounce.

        Returns: True if the player hits a boundary.   
        """
        hit: bool = False
        # If player crosses left border:
        if player.x_px < player.size_px:
            player.x_px = 2 * player.size_px - player.x_px
            player.angle = - player.angle
            player.speed *= self.elasticity
            hit = True

        # if player crosses right border:
        elif player.x_px > self.width_px - player.size_px:
            player.x_px = 2 * (self.width_px - player.size_px) - player.x_px
            player.angle = - player.angle
            player.speed *= self.elasticity
            hit = True

        # if player crosses top border:
        if player.y_px < player.size_px:
            player.y_px = 2 * player.size_px - player.y_px
            player.angle = math.pi - player.angle
            player.speed *= self.elasticity
            hit = True

        # if player crosses bottom border:
        elif player.y_px > self.height_px - player.size_px:
            player.y_px = 2 * (self.height_px - player.size_px) - player.y_px
            player.angle = math.pi - player.angle
            player.speed *= self.elasticity
            hit = True

        return hit
