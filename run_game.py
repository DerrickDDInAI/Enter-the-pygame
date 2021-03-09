"""
Game to demonstrate how:
- to write a game with python and pygame;
- to implement an AI model to solve the game by using neat module.
"""
# =====================================================================
# Import
# =====================================================================

import math
# Import internal modules
import random
import sys
from typing import Dict, List, Optional, Set, Tuple, TypedDict

import neat
from neat import population
# Import 3rd party modules
import pygame
from pygame.constants import TIMER_RESOLUTION

from gamecore.environment import Environment
# Import local modules
from gamecore.level import Level
from gamecore.player import AIBots, Gorilla, Obstacle, Player

# =====================================================================
# Classes
# =====================================================================

class GameWindow:
    """
    GameWindow has 3 attributes: window_dimensions_px, caption
    * window_dimensions_px: tuple of integers that specifies the window dimensions in pixels (width in px, height in px)
    * caption: string that is the title of the game
    """

    def __init__(self, window_dimensions_px, caption="game"):
        """
        Function to create an instance of GameWindow class
        By default:
        * caption is "game" if no caption is provided
        """
        self.caption = caption
        self.width_px, self.height_px = window_dimensions_px

        # Create a display surface called screen by convention
        self.screen = pygame.display.set_mode(
            (self.width_px, self.height_px), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    def display_caption(self):
        """
        Function to display the caption
        """
        pygame.display.set_caption(self.caption)


class Client:
    """
    Client is the user that controls a player.
    It has 1 attribute:
    * player: player that client controls.
    """

    def __init__(self, player) -> None:
        """
        Function to create an instance of Client class.
        """
        self.player = player

    def get_user_input(self):
        """
        Function to get user input.
        """
        # For event in the event queue since last call
        for event in pygame.event.get():

            # Check keys released for one instant
            if event.type == pygame.KEYUP:
                # Quit the game if you release the escape button
                if event.key == pygame.K_ESCAPE:
                    terminate()
                # Switch to next game session if you release the return button
                if event.key == pygame.K_RETURN:
                    return "change level"

            # Quit the game if you click on the X button at the top of the screen
            if event.type == pygame.QUIT:
                terminate()

            # Resize the display
            if event.type == pygame.VIDEORESIZE:
                game_window.screen = pygame.display.set_mode(
                    event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                return event.dict['size']

        # Check keys continuously pressed (needs to be outside of the for loop otherwise it would only be executed once per event in the event queue)
        keys = pygame.key.get_pressed()
        if keys:
            if keys[pygame.K_LEFT]:
                self.player.angle, self.player.speed = world.add_vectors(
                    (self.player.angle, self.player.speed), (- 1 * math.pi/2, 2))
            elif keys[pygame.K_RIGHT]:
                self.player.angle, self.player.speed = world.add_vectors(
                    (self.player.angle, self.player.speed), (math.pi/2, 2))
            if keys[pygame.K_UP]:
                self.player.angle, self.player.speed = world.add_vectors(
                    (self.player.angle, self.player.speed), (0, 2))
            elif keys[pygame.K_DOWN]:
                self.player.angle, self.player.speed = world.add_vectors(
                    (self.player.angle, self.player.speed), (math.pi, 2))
    
        # Limits player_1's speed
        if self.player.speed > 20:
            self.player.speed = 20

    def wait_for_pressed_key(self) -> Optional[bool]:
        """
        Function to check if any key is pressed.
        """
        # For event in the event queue since last call
        for event in pygame.event.get():

            # Check keys released for one instant
            if event.type == pygame.KEYUP:
                # Quit the game if you release the escape button
                if event.key == pygame.K_ESCAPE:
                    terminate()

            # Quit the game if you click on the X button at the top of the screen
            if event.type == pygame.QUIT:
                terminate()

            # Resize the display
            if event.type == pygame.VIDEORESIZE:
                game_window.screen = pygame.display.set_mode(
                    event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                return event.dict['size']

            # Check keys pressed for one instant
            if event.type == pygame.KEYDOWN:
                return True
# ============================================================
# Main functions
# ============================================================


def create_level(
    title: str,
    level_type: str,
    bg_image_path: Optional[str] = None,
    bg_color: Optional[Tuple[int]] = None,
    font_color: Tuple[int] = (22, 35, 46),
    resize: bool = False) -> Level:
    """
    Function to create a level.

    Returns: level.
    """

    # 1. Create Level instance
    level = Level(title, level_type, bg_surface_path=bg_image_path, bg_color=bg_color, font_color=font_color)

    # 2. If background image path is given, import it
    ## convert() is not necessary but converts the image into a format easier for pygame => faster
    if level.bg_surface_path:
        level.bg_surface = pygame.image.load(level.bg_surface_path).convert()

    # 3. If resize is True, resize the background image to the game_window size
    if resize:
        level.bg_surface = pygame.transform.scale(
        level.bg_surface, (game_window.width_px, game_window.height_px))

    return level

def terminate() -> None:
    """
    Function to quit the game and terminate the script.
    """
    pygame.quit()
    sys.exit()

def draw_text(text: str, color: Tuple[int], xy_pos_center_px: Tuple[int]) -> None:
    """
    Function to display text.

    Parameters:
    * text: text to display
    * color: font color
    * xy_pos_center_px: (x,y) coordinates of the center of text rectangle.
    """
    text_surface = game_font.render(
        text, True, color)  # text, True for anti-aliased text, color in rgb
    
    # Put the text in a rect to make it easier to display
    text_rect = text_surface.get_rect(center=xy_pos_center_px)

    # Draw the text on the game_window screen
    game_window.screen.blit(text_surface, text_rect)

def play_story_event(current_story_event: int, level: Level, gorilla_image: Optional[str]=None) -> None:
    """
    Function to play the story events.
    """
    # Fill the screen with level background color
    game_window.screen.fill(level.bg_color)
    draw_text(gorilla.dialogues[current_story_event], level.font_color, (
        game_window.width_px/2, game_window.height_px/2))
    gorilla.sounds.play()

    # If gorilla appears on the scene, draw its image or flipped image
    if gorilla_image == "gorilla_image":
        game_window.screen.blit(
            gorilla.image, (gorilla.x_px - gorilla.image.get_width(), gorilla.y_px - gorilla.image.get_height() - 100))
    elif gorilla_image == "gorilla_image_flip":
            game_window.screen.blit(gorilla.image_flip, (
                gorilla.x_px - gorilla.image.get_width(), gorilla.y_px - gorilla.image.get_height() - 100))

def start_screen(level: Level) -> None:
    """
    Function to start game at level 0: "Title" (slide).
    """
    # Variables
    start_screen = True
    time_s: float = 0.0
    current_story_event = -1  # title slide just before gorilla speaks
    transition_color = list(level.bg_color) # convert rgb tuple into a list to turn the screen whiter every second

    # Enter game loop
    while start_screen:
        # Get the delta t for one frame (this changes depending on system load).
        dt_s: float = float(main_clock.tick(framerate_limit) * 1e-3)
        
        # Get user input
        user_input = client_1.wait_for_pressed_key()

        # If user_input is a tuple, the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
        game_window.screen.blit(pygame.transform.scale(level.bg_surface, (game_window.width_px, game_window.height_px)), (0, 0))

        # If user_input is True, the user pressed a key to go forward in the story
        if user_input == True:
            current_story_event += 1

        # 1. Big text appears
        if current_story_event in [0, 1, 2]:
            play_story_event(current_story_event, level)

        # 2. Gorilla appears from the right of the screen
        elif current_story_event == 3:
            play_story_event(current_story_event, level, "gorilla_image")

        # 3. Gorilla speaks
        elif current_story_event in [4, 5, 6, 7]:
            play_story_event(current_story_event, level, "gorilla_image")

        # 4. Gorilla turns its back and speaks
        elif current_story_event in [8, 9]:
            play_story_event(current_story_event, level, "gorilla_image_flip")

        # 5. Gorilla faces towards left again and speaks
        elif current_story_event in [10, 11, 12, 13]:
            play_story_event(current_story_event, level, "gorilla_image")

        # 6. Gorilla turn its back and leaves the screen from the right
        elif current_story_event == 14:
            play_story_event(current_story_event, level, "gorilla_image_flip")

        # Transition before quitting the start screen loop
        elif current_story_event == 15:
            
            # Turn the screen whiter every second
            if time_s > 0.001:
                for i, color in enumerate(transition_color):
                    if color < 255:
                        transition_color[i] += 1
                        print(color)
                time_s = 0.0 # reset timer
            game_window.screen.fill(transition_color)
        
        # Quit the start screen loop
        elif current_story_event == 16:
            # stop gorilla sounds
            gorilla.sounds.stop()
            start_screen = False

        # Update the screen with the drawings
        pygame.display.update()

        # Time
        ## Measure time spent at each iteration
        time_s += dt_s
        ## Limit the frame rate to max the framerate_limit
        main_clock.tick(framerate_limit)

def game_1(genomes, config) -> None:
    """
    Function to play game 1 for current genome of AIBots.
    Game 1 objective: AIBots must avoid being touched by player or obstacles.
    1. Create population of AIBots. Each AIBots has its own neural network.
    2. Run the game for that population and set their respective fitness scores based on how long they survive.
    """
    # Global
    global generation
    generation += 1  # Increment by 1 at every game session

    # Variables
    game_running: bool = True  # Game loop
    time_s: float = 0.0
    player_1.x_px, player_1.y_px = (100, world.height_px/2)  # Restart player position at every game session

    # Instantiate obstacles
    obstacles_list: List[Obstacle] = []
    for obs_nb in range(5):
        obstacle = Obstacle(str(obs_nb), (random.uniform(0, world.width_px), random.uniform(
            0, world.height_px)), size_px=random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE), mass=50)
        obstacles_list.append(obstacle)

    # Create empty lists
    genomes_list: list = []
    aibots_list: List[AIBots] = []
    neural_nets_list: list = []

    # Create a population of AIBots and assign them a neural network
    for genome_id, genome in genomes:
        genome.fitness = 0  # AIBot starts the game with fitness score at 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets_list.append(net)
        # Create an aibot
        aibot_y_px = world.height_px/2
        aibots_list.append(
            AIBots(str(genome_id), (world.width_px - 100, aibot_y_px), size_px=AIBOT_SIZE, mass=50))
        genomes_list.append(genome)

    # Enter game loop; game continues until there is no more AIBots
    while game_running and len(aibots_list):

        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get user input
        user_input = client_1.get_user_input()

        # Go to next generation if player press return button
        if isinstance(user_input, str):
            break

        # Display background
        ## Display level 1 background surface
        ## blit() to display a surface on another surface: here to display level surface on screen
        ## (0,0): the position of the top left of bg_surface
        
        ## If user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
            world.width_px, world.height_px = user_input  # update the environment as well
        game_window.screen.fill(level_1.bg_color)  # fill the screen with level color

        # Reward each AIBot a fitness of 0.1 for each frame it stays alive
        for i, aibot in enumerate(aibots_list):
            genomes_list[i].fitness += 0.1

        # Give inputs => neural network will output a list of values
        # From which it can determine in which direction to move
        # Use a tanh activation function to have the output results between -1 and 1

            # As input: AIBot's location and its distance compared to player and obstacles
            distances_to_obstacles = []
            for obstacle in obstacles_list:
                distances_to_obstacles.extend([abs(aibot.x_px - obstacle.x_px), abs(aibot.y_px - obstacle.y_px)])
            
            input_list: list = [aibot.x_px,
                aibot.y_px,
                abs(aibot.x_px - client_1.player.x_px),
                abs(aibot.y_px - client_1.player.y_px)
                ]
            input_list.extend(distances_to_obstacles)

            # Activate AIBots's neural network to compute its output (= decision)
            output: list = neural_nets_list[i].activate(input_list)

            # Move AIBot
            ## If 1st output > 50%: go left
            if output[0] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (- 1 * math.pi/2, 2))
            
            ## If 2nd output > 50%: go right
            if output[1] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi/2, 2))

            ## If 3rd output > 50%: go up
            if output[2] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (0, 2))
            
            ## If 4th output > 50%: go down
            if output[3] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi, 2))

            aibot.move()
            world.add_air_resistance(aibot)
            world.attraction(player_1, aibot)
            world.bounce(aibot)

            collide_player: bool = world.collide(player_1, aibot, False) # False not to apply collision effect
            for obstacle in obstacles_list:
                collide_obstacle_aibot: bool = world.collide(obstacle, aibot, False)
                # If collision, punish the aibot and remove it
                if collide_player or collide_obstacle_aibot:
                    genomes_list[aibots_list.index(aibot)].fitness -= 5
                    neural_nets_list.pop(aibots_list.index(aibot))
                    genomes_list.pop(aibots_list.index(aibot))
                    aibots_list.pop(aibots_list.index(aibot))
                    break

            ## Limits aibot's speed
            if aibot.speed > 20:
                aibot.speed = 20

        # Move player
        player_1.move()
        world.add_air_resistance(player_1)
        world.bounce(player_1)

        # Move obstacles
        for obstacle in obstacles_list:
            obstacle.move()
            world.add_air_resistance(obstacle)
            world.collide(obstacle, player_1, True)
            world.bounce(obstacle)

            # Limits obstacle's speed
            if obstacle.speed > 20:
                obstacle.speed = 20

        # Draw
        ## Draw AIBots
        for aibot in aibots_list:
            pygame.draw.circle(game_window.screen, aibot.color,
                               (aibot.x_px, aibot.y_px), aibot.size_px)
            
        ## Draw Obstacles
        for obstacle in obstacles_list:
            pygame.draw.circle(game_window.screen, obstacle.color,
                               (obstacle.x_px, obstacle.y_px), obstacle.size_px)

        ## Draw Players
        pygame.draw.circle(game_window.screen, player_1.color,
                           (player_1.x_px, player_1.y_px), player_1.size_px)

        ## Draw text: level name
        draw_text(f"{level_1.name}", becode_color,
                  (200, 50))

        ## Draw text: Time
        draw_text(f"Time: {int(time_s)}", becode_color,
                  (game_window.width_px - 100, 50))

        ## Draw text: current generation
        draw_text(f"Generation: {generation}",
                  becode_color, (game_window.width_px/2, 50))

        ## Draw text: Number of AIBots alive
        draw_text(f"Alive: {len(aibots_list)}",
                  becode_color, (game_window.width_px/2, 100))

        # Update the screen with the drawings
        pygame.display.update()

        # Time
        time_s += dt_s  # Measure time spent
        # Limit the frame rate to max the framerate_limit
        main_clock.tick(framerate_limit)

def game_2(genomes, config) -> None:
    """
    Function to play game 2 for current genome of AIBots.
    Game 2 objective: AIBots must score goals by putting obstacle into the goal
    1. Create population of AIBots. Each AIBots has its own neural network.
    2. Run the game for that population and set their respective fitness scores based on how long they survive.
    """
    # Global
    global generation
    generation += 1  # Increment by 1 at every game session

    # Constants
    # GAMESIZE = 10
    OUTSIDE = 30
    # WINDOWWIDTH = (110 * GAMESIZE) + OUTSIDE # (Football field in m * GAMESIZE) + Outside area
    # WINDOWHEIGHT = (75 * GAMESIZE) + OUTSIDE
    LINEWIDTH = round(1.2 * 5)
    GOALSIZE = round(7.32 * 50)
    CIRCLE_RADIUS = 200
    LINECOLOR = (255, 255, 255)


    # Variables
    game_running: bool = True  # Game loop
    time_s: float = 0.0
    timer: float = 3.0
    score_left: int = 0
    score_right: int = 0
    score_left_bool: bool = False
    score_right_bool: bool = False

    # Instantiate obstacle (= ball in this game) at the center
    obstacles_list: List[Obstacle] = []
    for obs_nb in range(1):
        obstacle = Obstacle(str(obs_nb), (world.width_px/2,world.height_px/2), size_px=OBSTACLE_MIN_SIZE, mass=50)
        obstacles_list.append(obstacle)

    # Create empty lists
    genomes_list: list = []
    aibots_list: List[AIBots] = []
    neural_nets_list: list = []

    # Create a population of AIBots and assign them a neural network
    for genome_id, genome in genomes:
        genome.fitness = 0  # AIBot starts the game with fitness score at 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets_list.append(net)
        # create an aibot
        aibot_x = 100 + (world.width_px - 200)*(genome_id%2) # aibot starts at the right of screen if its id is odd and at the left if even
        # aibot_y = random.uniform(aibot_size_px, world.height - aibot_size_px)
        aibot_y = world.height_px/2
        aibots_list.append(
            AIBots(str(genome_id),(aibot_x, aibot_y), size_px=AIBOT_SIZE, mass=50, color=(255*(genome_id%2), 0, 0))) 
        genomes_list.append(genome)

    # Enter game loop
    while game_running and timer > 0.0:

        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get user input
        user_input = client_1.get_user_input()

        # Go to next generation if player press return button
        if isinstance(user_input, str):
            break

        # Display background
        ## Display level 1 background surface
        ## blit() to display a surface on another surface: here to display level surface on screen
        ## (0,0): the position of the top left of bg_surface
        
        ## If user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
            world.width_px, world.height_px = user_input  # update the environment as well
        game_window.screen.fill(level_2.bg_color)  # fill the screen with level color
        
        for i, aibot in enumerate(aibots_list):

        # Give inputs => neural network will output a list of values
        # From which it can determine in which direction to move
        # Use a tanh activation function to have the output results between -1 and 1

            # As input: AIBot's location and its distance compared to other AIBots and obstacle (= ball)
            input_list: list = [aibot.x_px, aibot.y_px]

            distance_between_bots = []
            for j, other_aibot in enumerate(aibots_list):
                if i != j:
                    distance_between_bots.extend([abs(aibot.x_px - other_aibot.x_px), abs(aibot.y_px - other_aibot.y_px)])
            
            input_list.extend(distance_between_bots)

            # Add input: its distance compared to obstacle (= ball)
            # and distance between obstacle and goal
            distances_to_obstacles = []
            distances_obst_goal = []
            for obstacle in obstacles_list:
                distances_to_obstacles.extend([abs(aibot.x_px - obstacle.x_px), abs(aibot.y_px - obstacle.y_px)])
                distances_obst_goal.extend([obstacle.x_px, obstacle.y_px])
            input_list.extend(distances_to_obstacles)

            # Activate AIBots's neural network to compute its output (= decision)
            output: list = neural_nets_list[i].activate(input_list)

            # Move AIBot
            ## If 1st output > 50%: go left
            if output[0] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (- 1 * math.pi/2, 2))
            
            ## If 2nd output > 50%: go right
            if output[1] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi/2, 2))

            ## If 3rd output > 50%: go up
            if output[2] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (0, 2))
            
            ## If 4th output > 50%: go down
            if output[3] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi, 2))

            aibot.move()
            world.add_air_resistance(aibot)
            world.attraction(player_1, aibot)
            world.bounce(aibot)

            for j, other_aibot in enumerate(aibots_list):
                if i != j:
                    world.collide(aibot, other_aibot, True)
            
            # Limits aibot's speed
            if aibot.speed > 20:
                aibot.speed = 20

            # Move obstacle (= ball)
            for obstacle in obstacles_list:
                obstacle.move()
                world.add_air_resistance(obstacle)
                world.bounce(obstacle)
                collide_obstacle_aibot: bool = world.collide(obstacle, aibot, True)
                # If collision, reward the aibot
                if collide_obstacle_aibot:
                    genomes_list[aibots_list.index(aibot)].fitness += 2

                # Limits obstacle's speed
                if obstacle.speed > 20:
                    obstacle.speed = 20
            
            # If ball enters right goal, left team scores a goal
            if (obstacle.x_px >= world.width_px - obstacle.size_px - 10) and (
                obstacle.y_px > world.height_px/2 - GOALSIZE/2) and (
                    obstacle.y_px < world.height_px/2 + GOALSIZE/2):
                score_left_bool = True
            if (obstacle.x_px <= obstacle.size_px + 10)  and (
                obstacle.y_px > world.height_px/2 - GOALSIZE/2) and (
                    obstacle.y_px < world.height_px/2 + GOALSIZE/2):
                score_right_bool = True # right team scores a goal

        # If score, reset positions and update score status
        if score_left_bool or score_right_bool:
            whistle_sound.play()
            if score_left_bool:
                score_left += 1 # left team scores a goal
                
                # Reward left team
                for i, aibot in enumerate(aibots_list, 1):
                    if i%2 == 0:
                        genomes_list[aibots_list.index(aibot)].fitness += 5
                    else:
                        genomes_list[aibots_list.index(aibot)].fitness -= 5
                score_left_bool = False

            if score_right_bool:
                score_right += 1 # right team scores a goal
                
                # Reward right team
                for i, aibot in enumerate(aibots_list, 1):
                    if i%2 != 0:
                        genomes_list[aibots_list.index(aibot)].fitness += 5
                    else:
                        genomes_list[aibots_list.index(aibot)].fitness -= 5
                score_right_bool = False

            ## Reset position after every goal
            for obstacle in obstacles_list:
                obstacle.x_px, obstacle.y_px = (world.width_px/2, world.height_px/2)
                obstacle.angle = 0
                obstacle.speed = 0

            for i, aibot in enumerate(aibots_list, 1):
                aibot.x_px = 100 + (world.width_px - 200)*(genome_id%2)
                aibot.y_px = world.height_px/2
                aibot.angle = 0
                aibot.speed = 0

        # If no score, punish them every second
        elif time_s >= 1.0:
            for aibot in aibots_list:
                genomes_list[aibots_list.index(aibot)].fitness -= 1

        # Draw
        ## Draw football field
        pygame.draw.rect(game_window.screen, LINECOLOR, (OUTSIDE, OUTSIDE, world.width_px - OUTSIDE * 2, world.height_px - OUTSIDE * 2), LINEWIDTH)
        pygame.draw.rect(game_window.screen, LINECOLOR, (0, world.height_px/2 - GOALSIZE/2, OUTSIDE, GOALSIZE), LINEWIDTH)
        pygame.draw.rect(game_window.screen, LINECOLOR, (world.width_px - OUTSIDE, world.height_px/2 - GOALSIZE/2, OUTSIDE, GOALSIZE), LINEWIDTH)
        pygame.draw.line(game_window.screen, LINECOLOR, (world.width_px/2, OUTSIDE), (world.width_px/2, world.height_px - OUTSIDE), LINEWIDTH)
        pygame.draw.circle(game_window.screen, LINECOLOR, (world.width_px/2, world.height_px/2), CIRCLE_RADIUS, LINEWIDTH)

        ## Draw AIBots
        for aibot in aibots_list:
            pygame.draw.circle(game_window.screen, aibot.color,
                               (aibot.x_px, aibot.y_px), aibot.size_px)
            
        ## Draw Obstacles
        for obstacle in obstacles_list:
            pygame.draw.circle(game_window.screen, obstacle.color,
                               (obstacle.x_px, obstacle.y_px), obstacle.size_px)

        ## Draw text: level name
        draw_text(f"{level_2.name}", becode_color,
                  (100, 50))

        ## Draw text: Time
        draw_text(f"Timer: {int(timer)}", becode_color,
                  (game_window.width_px - 100, 50))

        ## Draw text: current generation
        draw_text(f"Generation: {generation}",
                  becode_color, (game_window.width_px/2, 50))

        ## Draw text: Number of AIBots alive
        draw_text(f"Score: {score_left} - {score_right}",
                  becode_color, (game_window.width_px/2, 100))

        # Update the screen with the drawings
        pygame.display.update()
        # pygame.display.flip() # difference between flip() and update(): flip updates the entire screen; update(rect) you can update portion of the display

        # Time
        time_s += dt_s  # Measure time spent
        if time_s > 1.0:
            timer -= 1.0
            time_s = 0.0
        # Limit the frame rate to max the framerate_limit
        main_clock.tick(framerate_limit)

def game_3(genomes, config) -> None:
    """
    Function to play game 3 for current genome of AIBots.
    Game 3 objective: AIBots must touch the player and avoid obstacles.
    1. Create population of AIBots. Each AIBots has its own neural network.
    2. Run the game for that population and set their respective fitness scores based on how long they survive.
    """
    # Global
    global generation
    generation += 1  # Increment by 1 at every game session

    # Variables
    game_running: bool = True  # Game loop
    time_s: float = 0.0
    player_1.x_px, player_1.y_px = (100, world.height_px/2)  # Restart player position at every game session

    # Instantiate obstacles
    obstacles_list: List[Obstacle] = []
    for obs_nb in range(15):
        obstacle = Obstacle(str(obs_nb), (random.uniform(0, world.width_px), random.uniform(
            0, world.height_px)), size_px=random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE), mass=50)
        obstacles_list.append(obstacle)

    # Create empty lists
    genomes_list: list = []
    aibots_list: List[AIBots] = []
    neural_nets_list: list = []

    # Create a population of AIBots and assign them a neural network
    for genome_id, genome in genomes:
        genome.fitness = 0  # AIBot starts the game with fitness score at 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets_list.append(net)
        # Create an aibot
        aibot_y_px = world.height_px/2
        aibots_list.append(
            AIBots(str(genome_id), (world.width_px - 100, aibot_y_px), size_px=AIBOT_SIZE, mass=50))
        genomes_list.append(genome)

    # Enter game loop; game continues until there is no more AIBots
    while game_running and len(aibots_list):

        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get user input
        user_input = client_1.get_user_input()

        # Go to next generation if player press return button
        if isinstance(user_input, str):
            break

        # Display background
        ## Display level 1 background surface
        ## blit() to display a surface on another surface: here to display level surface on screen
        ## (0,0): the position of the top left of bg_surface
        
        ## If user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
            world.width_px, world.height_px = user_input  # update the environment as well
        game_window.screen.fill(level_3.bg_color)  # fill the screen with level color

        # Reward each AIBot a fitness of 0.1 for each frame it stays alive
        for i, aibot in enumerate(aibots_list):
            genomes_list[i].fitness += 0.1

        # Give inputs => neural network will output a list of values
        # From which it can determine in which direction to move
        # Use a tanh activation function to have the output results between -1 and 1

            # As input: AIBot's location and its distance compared to player and obstacles
            distances_to_obstacles = []
            for obstacle in obstacles_list:
                distances_to_obstacles.extend([abs(aibot.x_px - obstacle.x_px), abs(aibot.y_px - obstacle.y_px)])
            
            input_list: list = [aibot.x_px,
                aibot.y_px,
                abs(aibot.x_px - client_1.player.x_px),
                abs(aibot.y_px - client_1.player.y_px)
                ]
            input_list.extend(distances_to_obstacles)

            # Activate AIBots's neural network to compute its output (= decision)
            output: list = neural_nets_list[i].activate(input_list)

            # Move AIBot
            ## If 1st output > 50%: go left
            if output[0] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (- 1 * math.pi/2, 2))
            
            ## If 2nd output > 50%: go right
            if output[1] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi/2, 2))

            ## If 3rd output > 50%: go up
            if output[2] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (0, 2))
            
            ## If 4th output > 50%: go down
            if output[3] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi, 2))

            aibot.move()
            world.add_air_resistance(aibot)
            world.attraction(player_1, aibot)
            world.bounce(aibot)

            collide_player: bool = world.collide(player_1, aibot, True) # True to apply collision effect
            if collide_player:
                genomes_list[aibots_list.index(aibot)].fitness += 5
            for obstacle in obstacles_list:
                collide_obstacle_aibot: bool = world.collide(obstacle, aibot, False)
                # If collision, punish the aibot and remove it
                if collide_obstacle_aibot:
                    genomes_list[aibots_list.index(aibot)].fitness -= 5
                    neural_nets_list.pop(aibots_list.index(aibot))
                    genomes_list.pop(aibots_list.index(aibot))
                    aibots_list.pop(aibots_list.index(aibot))
                    break

            ## Limits aibot's speed
            if aibot.speed > 20:
                aibot.speed = 20

        # Move player
        player_1.move()
        world.add_air_resistance(player_1)
        world.bounce(player_1)

        # Move obstacles
        for obstacle in obstacles_list:
            obstacle.move()
            world.add_air_resistance(obstacle)
            world.collide(obstacle, player_1, True)
            world.bounce(obstacle)

            # Limits obstacle's speed
            if obstacle.speed > 20:
                obstacle.speed = 20

        # Draw
        ## Draw AIBots
        for aibot in aibots_list:
            pygame.draw.circle(game_window.screen, aibot.color,
                               (aibot.x_px, aibot.y_px), aibot.size_px)
            
        ## Draw Obstacles
        for obstacle in obstacles_list:
            pygame.draw.circle(game_window.screen, obstacle.color,
                               (obstacle.x_px, obstacle.y_px), obstacle.size_px)

        ## Draw Players
        pygame.draw.circle(game_window.screen, player_1.color,
                           (player_1.x_px, player_1.y_px), player_1.size_px)

        ## Draw text: level name
        draw_text(f"{level_3.name}", becode_color,
                  (200, 50))

        ## Draw text: Time
        draw_text(f"Time: {int(time_s)}", becode_color,
                  (game_window.width_px - 100, 50))

        ## Draw text: current generation
        draw_text(f"Generation: {generation}",
                  becode_color, (game_window.width_px/2, 50))

        ## Draw text: Number of AIBots alive
        draw_text(f"Alive: {len(aibots_list)}",
                  becode_color, (game_window.width_px/2, 100))

        # Update the screen with the drawings
        pygame.display.update()

        # Time
        time_s += dt_s  # Measure time spent
        # Limit the frame rate to max the framerate_limit
        main_clock.tick(framerate_limit)

def run(config_file, game):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))  # DD: this gets some stats
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    best_performer = population.run(game, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(best_performer))

# ============================================================
# Run
# ============================================================

if __name__ == '__main__':

    # Globals

    # CONSTANTS
    WINDOW_WIDTH_PX: int = 1440
    WINDOW_HEIGHT_PX: int = 900
    CAPTION: str = "Enter the Pygame"
    PLAYER_SIZE: int = 50
    AIBOT_SIZE: int = 50
    GORILLA_SIZE: int = 50
    OBSTACLE_MIN_SIZE: int = 20
    OBSTACLE_MAX_SIZE: int = 50

    # Variables
    framerate_limit: int = 120
    generation: int = 0
    slide_font_color: Tuple[int] = (255, 255, 255)
    becode_color: Tuple[int] = (22, 35, 46)

    # Setup
    pygame.init()  # initiate pygame
    pygame.font.init()  # initiate font
    game_font = pygame.font.SysFont("comicsans", 50) # setting font and size

    # Display
    game_window = GameWindow((WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX), CAPTION)
    game_window.display_caption()

    # Clock
    main_clock = pygame.time.Clock()  # instantiate clock to limit the frame rate

    # Instantiate environment
    world = Environment((WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX),
                        color=slide_font_color)
    

    # Instantiate player
    player_1 = Player(
        "John Titor",
        (100, world.height_px/2),
        size_px=PLAYER_SIZE,
        mass=100,
        color=becode_color
    )

    # Instantiate local client who will control player_1
    client_1 = Client(player_1)

    # Instantiate gorilla
    gorilla = Gorilla((game_window.width_px, game_window.height_px))
    gorilla.image = pygame.image.load("gamecore/assets/images/gorilla.png").convert_alpha()
    gorilla.image_flip = pygame.transform.flip(gorilla.image, True, False)
    
    # import gorilla sounds
    gorilla.sounds = pygame.mixer.Sound(
        "gamecore/assets/sounds/gorilla_sounds.mp3")
    
    # import whistle sound (for football game)
    whistle_sound = pygame.mixer.Sound(
        "gamecore/assets/sounds/whistle_sound.mp3")

    # Start screen: Title slide and dialogue with gorilla
    level_0 = create_level("Title", "slide", "gamecore/assets/images/title_slide.png", bg_color=becode_color, font_color= (255,255,255), resize=True)
    start_screen(level_0)

    # Start game_1
    level_1 = create_level("Don't touch a player!", "game_level", bg_color=(255,255,255))
    config_path = "gamecore/config-feedforward.txt"
    run(config_path, game_1)

    # Start game_3
    generation = 0 # reset generation counter
    level_3 = create_level("Touch a player!", "game_level", bg_color=(255,255,255))
    config_path = "gamecore/config-feedforward-3.txt"
    run(config_path, game_3)

    # Start game_2
    generation = 0 # reset generation counter
    level_2 = create_level("Football", "game_level", bg_color=(120,184,51))
    config_path = "gamecore/config-feedforward-2.txt"
    run(config_path, game_2)

    # Quit the program
    terminate()
