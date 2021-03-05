# =====================================================================
# Classes
# =====================================================================

# from pygame import math
import math
from typing import Tuple


class Environment:
    """
    Environment defines the physics and boundaries of the simulation. 
    """

    def __init__(self, size, color=(255, 255, 255)):
        self.width, self.height = size
        self.color = color
        self.air_mass = 0.02
        self.elasticity = 0.75
        self.gravity = 0.01
        self.acceleration = (math.pi, self.gravity)

    def add_vectors(self, vector_1, vector_2):
        """
        Function to add 2 vectors
        A vector has a magnitude and a direction
        Returns: sum of vector_1 and vector_2
        """
        angle_1, magnitude_1 = vector_1
        angle_2, magnitude_2 = vector_2
        x = math.sin(angle_1) * magnitude_1 + math.sin(angle_2) * magnitude_2
        y = math.cos(angle_1) * magnitude_1 + math.cos(angle_2) * magnitude_2

        angle = 0.5 * math.pi - math.atan2(y, x)
        magnitude = math.hypot(x, y)

        return (angle, magnitude)

    # def add_air_resistance(self, player):
    #     player.air_resistance = (player.mass/(player.mass + self.air_mass)) ** player.size

    def add_air_resistance(self, player):
        """
        Function to make the player experience air resistance
        that slows its speed.
        """
        player.speed *= (player.mass/(player.mass +
                                      self.air_mass)) ** player.size

    def accelerate(self, player, vector):
        """
        Accelerate (= change speed and/or angle) by a vector
        """
        player.angle, player.speed = self.add_vectors(
            (player.angle, player.speed), vector)

    def attraction(self, player_1, player_2):
        """
        To change the velocity (= speed and direction)
        due to gravitational attraction between 2 players
        """
        distance_x = player_1.x - player_2.x
        distance_y = player_1.y - player_2.y
        distance = math.hypot(distance_x, distance_y)

        # if distance < sum of players' radius, it means collision
        if distance < player_1.size + player_2.size:
            return True

        theta = math.atan2(distance_y, distance_x)
        # Newton’s law of gravity
        force = 0.1 * player_1.mass * player_2.mass / distance**2
        self.accelerate(player_1, (theta - 0.5 * math.pi, force/player_1.mass))
        self.accelerate(player_2, (theta + 0.5 * math.pi, force/player_2.mass))

    def collide(self, player_1, player_2) -> bool:
        """
        Function to check if collision between 2 players
        and if collision, make them bounce.

        Returns: True if collision
        """
        distance_x = player_1.x - player_2.x
        distance_y = player_1.y - player_2.y
        distance = math.hypot(distance_x, distance_y)

        # if distance < sum of players' radius, it means collision
        if distance < player_1.size + player_2.size:
            angle = math.atan2(distance_y, distance_x) + 0.5 * math.pi
            total_mass = player_1.mass + player_2.mass

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

            elasticity = player_1.elasticity * player_2.elasticity
            player_1.speed *= elasticity
            player_2.speed *= elasticity

            # At the time we detect the collision, the players circles could possibly overlap
            # We correct their positions to remove this overlap
            overlap = 0.5 * (player_1.size + player_2.size - distance + 1)
            player_1.x += math.sin(angle) * overlap
            player_1.y -= math.cos(angle) * overlap
            player_2.x -= math.sin(angle) * overlap
            player_2.y += math.cos(angle) * overlap

            return True

    def bounce(self, player) -> bool:
        """
        Function to check if a player hits the environment boundary
        and if so, make it bounce.

        Returns: True if the player hits a border    
        """
        hit = False
        # if player crosses left border:
        if player.x < player.size:
            player.x = 2 * player.size - player.x
            player.angle = - player.angle
            player.speed *= self.elasticity
            hit = True

        # if player crosses right border:
        elif player.x > self.width - player.size:
            player.x = 2 * (self.width - player.size) - player.x
            player.angle = - player.angle
            player.speed *= self.elasticity
            hit = True

        # if player crosses top border:
        if player.y < player.size:
            player.y = 2 * player.size - player.y
            player.angle = math.pi - player.angle
            player.speed *= self.elasticity
            hit = True

        # if player crosses bottom border:
        elif player.y > self.height - player.size:
            player.y = 2 * (self.height - player.size) - player.y
            player.angle = math.pi - player.angle
            player.speed *= self.elasticity
            hit = True

        return hit
