"""
Game to demonstrate how:
- to write a game with python and pygame;
- to implement an AI model to solve the game by using neat module.
"""
# =====================================================================
# Import
# =====================================================================

# Import internal modules
import random
import sys
import math
from typing import List, Set, Dict, TypedDict, Tuple, Optional

# Import 3rd party modules
import pygame
import neat
from pygame.constants import TIMER_RESOLUTION

# Import local modules
from gamecore.level import Level
from gamecore.environment import Environment
from gamecore.player import AIBots, Obstacle, Player, Gorilla


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
    Client 
    """

    def __init__(self, player):
        """
        Function to create an instance of Client class
        """
        self.player = player

    def get_user_input(self) -> Tuple[int, int]:
        """
        Function to get user input
        """

        for event in pygame.event.get():

            # Check keys released for one instant
            if event.type == pygame.KEYUP:
                # Quit the game if you release the escape button
                if event.key == pygame.K_ESCAPE:
                    terminate()
                
                if event.key == pygame.K_RETURN:
                    return "change level"

            # Quit the game if you click on the X button at the top of the screen
            if event.type == pygame.QUIT:
                terminate()

            # Check keys pressed for one instant
            if event.type == pygame.KEYDOWN:
                # Accelerate player if space bar is pressed and boost available
                if event.key == pygame.K_SPACE:  # and player.boost == 5.0:
                    pass

            # Resize the display
            if event.type == pygame.VIDEORESIZE:
                game_window.screen = pygame.display.set_mode(
                    event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                return event.dict['size']
                # game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, event.dict['size']), (0,0))
                # pygame.display.flip()

        # Check keys continuously pressed (needs to be outside of the for loop otherwise only be executed once per event in the event queue)
        keys = pygame.key.get_pressed()
        if keys:
            # vector = pygame.Vector2(0,0)
            if keys[pygame.K_LEFT]:
                # vector += pygame.Vector2(-1,2)
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

    def wait_for_pressed_key(self) -> bool:
        """
        Function to check if any key is pressed
        """
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
                # game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, event.dict['size']), (0,0))
                # pygame.display.flip()

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
    1. Create population of AIBots. Each AIBots has its own neural network.
    2. Run the game for that population and set their respective fitness scores based on how long they survive.
    """
    # Global
    global generation
    generation += 1  # Increment by 1 at every game session

    # Variables
    game_running: bool = True  # Game loop
    time_s: float = 0.0
    # current_level_index = 1 # level 1
    player_1.x, player_1.y = (100, world.height/2)  # Restart player position

    # Create empty lists
    genomes_list: list = []
    aibots_list: List[AIBots] = []
    neural_nets_list: list = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # AIBot starts the game with fitness score at 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets_list.append(net)
        # create an aibot with specific size and starting at random y position within boundaries included
        aibot_size = 100
        # aibot_y = random.uniform(aibot_size, world.height - aibot_size)
        aibot_y = world.height/2
        aibots_list.append(
            AIBots((world.width - 100, aibot_y), size=aibot_size, mass=50))
        genomes_list.append(genome)

    # Instantiate aibots
    # aibot_1 = AIBots((world.width - 100, world.height/2), size=50, mass=1)

    # Enter game loop
    while game_running and len(aibots_list):

        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get user input
        user_input = client_1.get_user_input()

        # Go to next generation if player press return button
        if isinstance(user_input, str):
            # game_running = False
            break

        # Display background
        # Display level 1 background surface
        # blit() to display a surface on another surface: here to display level surface on screen
        # (0,0): the position of the top left of bg_surface
        # if user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
            world.width, world.height = user_input  # update the environment as well
        game_window.screen.fill(world.color)  # fill the screen with white
        # game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, (game_window.width_px,game_window.height_px)), (0,0))
        # game_window.screen.blit(levels_list[current_level_index].bg_surface, (0,0))

        # Reward each AIBot a fitness of 0.1 for each frame it stays alive
        for i, aibot in enumerate(aibots_list):
            genomes_list[i].fitness += 0.1

        # get_ai_decision()
        # Give its location and its distance compared to player => neural network will output a list of values
        # From which it can determine in which direction to move
        # Use a tanh activation function to have the output results between -1 and 1
            # output: list = neural_nets_list[i].activate((aibot.x, aibot.y, abs(
            #     aibot.x - client_1.player.x), abs(aibot.y - client_1.player.y)))
            
            # As input: its location and its distance compared to player and other bots
            # distance_between_bots = []
            # for j, other_aibot in enumerate(aibots_list):
            #     if i != j:
            #         distance_between_bots.extend([abs(aibot.x - other_aibot.x), abs(aibot.y - other_aibot.y)])
            
            # input_list: list = [aibot.x,
            #     aibot.y,
            #     abs(aibot.x - client_1.player.x),
            #     abs(aibot.y - client_1.player.y)
            #     ]
            # input_list.extend(distance_between_bots)
            # # print(len(input_list)) # should be 4 + (2*99) = 200
            # output: list = neural_nets_list[i].activate(input_list)

            # As input: its location and its distance compared to player and obstacles
            distances_to_obstacles = []
            for obstacle in obstacles_list:
                distances_to_obstacles.extend([abs(aibot.x - obstacle.x), abs(aibot.y - obstacle.y)])
            
            input_list: list = [aibot.x,
                aibot.y,
                abs(aibot.x - client_1.player.x),
                abs(aibot.y - client_1.player.y)
                ]
            input_list.extend(distances_to_obstacles)
            # print(len(input_list)) # should be 4 + (2*30)
            output: list = neural_nets_list[i].activate(input_list)

            # if output[0] > 0.5: go left
            if output[0] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (- 1 * math.pi/2, 2))
            if output[1] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi/2, 2))
            if output[2] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (0, 2))
            if output[3] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi, 2))

            # Limits aibot's speed
            if aibot.speed > 20:
                aibot.speed = 20

            aibot.move()
            world.add_air_resistance(aibot)
            world.attraction(player_1, aibot)
            world.bounce(aibot)
            # bounce: bool = world.bounce(aibot)
            # If hits a border, punish the aibot to prevent him from just staying at the border
            # if bounce:
            #     genomes_list[i].fitness -= 3

            collide_player: bool = world.collide(player_1, aibot, False)
            for obstacle in obstacles_list:
                collide_obstacle_aibot: bool = world.collide(obstacle, aibot, True)
                # If collision, punish the aibot and remove it
                if collide_player or collide_obstacle_aibot:
                    genomes_list[aibots_list.index(aibot)].fitness -= 5
                    neural_nets_list.pop(aibots_list.index(aibot))
                    genomes_list.pop(aibots_list.index(aibot))
                    aibots_list.pop(aibots_list.index(aibot))
                    break
            
            # for other_aibot in aibots_list[i+1:len(aibots_list) - 1]:
            #     collide_otherbot: bool = world.collide(aibot, other_aibot, True)
            #     if collide_otherbot:
            #         genomes_list[aibots_list.index(aibot)].fitness -= 3
            #         genomes_list[aibots_list.index(other_aibot)].fitness -= 3

            # If collision, punish the aibot and remove it
            # if collide_player:
            #     genomes_list[aibots_list.index(aibot)].fitness -= 5
            #     neural_nets_list.pop(aibots_list.index(aibot))
            #     genomes_list.pop(aibots_list.index(aibot))
            #     aibots_list.pop(aibots_list.index(aibot))

        player_1.move()
        world.add_air_resistance(player_1)
        world.bounce(player_1)

        for obstacle in obstacles_list:
            obstacle.move()
            world.add_air_resistance(obstacle)
            world.collide(obstacle, player_1, True)
            world.bounce(obstacle)
            # Limits obstacle's speed
            if obstacle.speed > 20:
                obstacle.speed = 20

            
        # Draw Obstacles
        for obstacle in obstacles_list:
            pygame.draw.circle(game_window.screen, obstacle.color,
                               (obstacle.x, obstacle.y), obstacle.size)

        # Draw Players
        pygame.draw.circle(game_window.screen, player_1.color,
                           (player_1.x, player_1.y), player_1.size)

        # Draw AIBots
        for aibot in aibots_list:
            pygame.draw.circle(game_window.screen, aibot.color,
                               (aibot.x, aibot.y), aibot.size)

        # Draw text
        # Time
        draw_text(f"Time: {int(time_s)}", becode_color,
                  (game_window.width_px - 100, 50))

        # current generations
        draw_text(f"Generation: {generation}",
                  becode_color, (game_window.width_px/2, 50))

        # Number of AIBots alive
        draw_text(f"Alive: {len(aibots_list)}",
                  becode_color, (game_window.width_px/2, 100))

        # Update the screen with the drawings
        pygame.display.update()
        # pygame.display.flip() # difference between flip() and update(): flip updates the entire screen; update(rect) you can update portion of the display

        # Time
        time_s += dt_s  # Measure time spent
        # Limit the frame rate to max the framerate_limit
        main_clock.tick(framerate_limit)

def game_2(genomes, config) -> None:
    """
    Function to play game 2 for current genome of AIBots.
    1. Create population of AIBots. Each AIBots has its own neural network.
    2. Run the game for that population and set their respective fitness scores based on how long they survive.
    """
    # Global
    global generation
    generation += 1  # Increment by 1 at every game session

    # Variables
    game_running: bool = True  # Game loop
    time_s: float = 0.0
    timer: float = 3.0
    score_left: int = 0
    score_right: int = 0
    score_left_bool: bool = False
    score_right_bool: bool = False
    
    # Set obstacle (= ball in this game) at the center
    for obstacle in obstacles_list:
        obstacle.x = world.width/2
        obstacle.y = world.height/2

    # Create empty lists
    genomes_list: list = []
    aibots_list: List[AIBots] = []
    neural_nets_list: list = []

    for genome_id, genome in genomes:
        print(genome_id)
        genome.fitness = 0  # AIBot starts the game with fitness score at 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets_list.append(net)
        # create an aibot with specific size and starting at random y position within boundaries included
        aibot_size = 50
        aibot_x = 100 + (world.width - 200)*(genome_id%2) # aibot starts at the right of screen if its id is odd and at the left if even
        # aibot_y = random.uniform(aibot_size, world.height - aibot_size)
        aibot_y = world.height/2
        aibots_list.append(
            AIBots((aibot_x, aibot_y), size=aibot_size, mass=50, color=(255*(genome_id%2), 0, 0))) 
        genomes_list.append(genome)

    # Enter game loop
    while game_running and timer > 0:

        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get user input
        user_input = client_1.get_user_input()

        # Display background
        # Display level 1 background surface
        # blit() to display a surface on another surface: here to display level surface on screen
        # (0,0): the position of the top left of bg_surface
        # if user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
            world.width, world.height = user_input  # update the environment as well
        game_window.screen.fill(world.color)  # fill the screen with white
        # game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, (game_window.width_px,game_window.height_px)), (0,0))
        # game_window.screen.blit(levels_list[current_level_index].bg_surface, (0,0))

        # Go to next generation if player press return button
        if isinstance(user_input, str):
            # game_running = False
            break
        
        for i, aibot in enumerate(aibots_list):
            # Reward each AIBot a fitness of 0.1 for each frame it stays alive
            # genomes_list[i].fitness += 0.1

        # Give its location and its distance compared to player => neural network will output a list of values
        # From which it can determine in which direction to move
        # Use a tanh activation function to have the output results between -1 and 1
            # As input: its location and its distance compared to other bots
            # input_list: list = [gorilla_left.x, gorilla_left.y, gorilla_right.x, gorilla_right.y]
            input_list: list = []
            distance_between_bots = []
            for j, other_aibot in enumerate(aibots_list):
                if i != j:
                    distance_between_bots.extend([abs(aibot.x - other_aibot.x), abs(aibot.y - other_aibot.y)])
            
            input_list.extend(distance_between_bots)

            # Add input: its distance compared to obstacles
            distances_to_obstacles = []
            distances_obst_goal = []
            for obstacle in obstacles_list:
                distances_to_obstacles.extend([abs(aibot.x - obstacle.x), abs(aibot.y - obstacle.y)])
                distances_obst_goal.extend([obstacle.x, obstacle.y])
            input_list.extend(distances_to_obstacles)
            
            output: list = neural_nets_list[i].activate(input_list)

            # if output[0] > 0.5: go left
            if output[0] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (- 1 * math.pi/2, 2))
            if output[1] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi/2, 2))
            if output[2] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (0, 2))
            if output[3] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi, 2))

            aibot.move()
            world.add_air_resistance(aibot)
            world.attraction(player_1, aibot)
            world.bounce(aibot)
            # bounce: bool = world.bounce(aibot)
            # If hits a border, punish the aibot to prevent him from just staying at the border
            # if bounce:
            #     genomes_list[i].fitness -= 3
            for j, other_aibot in enumerate(aibots_list):
                if i != j:
                    world.collide(aibot, other_aibot, True)
                    # if collide_otherbot:
                    #     genomes_list[aibots_list.index(aibot)].fitness -= 1
                    #     # genomes_list[aibots_list.index(other_aibot)].fitness -= 1
            
            # Limits aibot's speed
            if aibot.speed > 20:
                aibot.speed = 20

            for obstacle in obstacles_list:
                obstacle.move()
                world.add_air_resistance(obstacle)
                world.bounce(obstacle)
                collide_obstacle_aibot: bool = world.collide(obstacle, aibot, True)
                # If collision, reward the aibot
                if collide_obstacle_aibot:
                    genomes_list[aibots_list.index(aibot)].fitness += 2
                
                # Check if obstacle collides with gorilla_right or gorilla_left
                # distance_gorilla_right = (round(obstacle.x - gorilla_right.x), round(obstacle.y - gorilla_right.y))
                # distance_gorilla_left = (round(obstacle.x - gorilla_left.x), round(obstacle.y - gorilla_left.y))
                # obstacle_rect = pygame.draw.circle(game_window.screen, obstacle.color,
                # (obstacle.x, obstacle.y), obstacle.size)
                # obstacle_rect = pygame.mask.Mask(obstacle_rect.size, True)
                # if gorilla_right.image_mask.overlap(obstacle_rect, distance_gorilla_right) and (i+1)%2 == 0: # and if aibot must shoot at gorilla_right
                #     genomes_list[aibots_list.index(aibot)].fitness += 5
                #     score_left_bool = True # left team scores a goal
                #     print("yes")
                # elif gorilla_right.image_mask.overlap(obstacle_rect, distance_gorilla_right) and (i+1)%2 != 0: # and if aibot must shoot at gorilla_left
                #     genomes_list[aibots_list.index(aibot)].fitness -= 5 # punish as it shoots at wrong gorilla
                #     score_left_bool = True # left team scores a goal
                # if gorilla_left.image_mask.overlap(obstacle_rect, distance_gorilla_left) and (i+1)%2 != 0: # and if aibot must shoot to gorilla_left
                #     genomes_list[aibots_list.index(aibot)].fitness += 5
                #     score_right_bool: True # right team scores a goal
                # elif gorilla_left.image_mask.overlap(obstacle_rect, distance_gorilla_left) and (i+1)%2 == 0: # and if aibot must shoot to gorilla_left
                #     genomes_list[aibots_list.index(aibot)].fitness -= 5 # punish as it shoots at wrong gorilla
                #     score_right_bool: True # right team scores a goal

                # if gorilla_right.image_mask.overlap(obstacle_rect, distance_gorilla_right):
                #     score_left_bool = True # left team scores a goal
                # if gorilla_right.image_mask.overlap(obstacle_rect, distance_gorilla_right):
                #     score_left_bool = True # left team scores a goal
                # if gorilla_left.image_mask.overlap(obstacle_rect, distance_gorilla_left):
                #     score_right_bool = True # right team scores a goal
                # if gorilla_left.image_mask.overlap(obstacle_rect, distance_gorilla_left):
                #     score_right_bool = True # right team scores a goal

                # Limits obstacle's speed
                if obstacle.speed > 20:
                    obstacle.speed = 20
            

            if obstacle.x >= world.width - obstacle.size - 10:
                score_left_bool = True # left team scores a goal
            if obstacle.x <= obstacle.size + 10:
                score_right_bool = True # right team scores a goal

        # if score, reset positions and score states
        if score_left_bool or score_right_bool:
            print("score")
            if score_left_bool:
                score_left += 1 # left team scores a goal
                for i, aibot in enumerate(aibots_list, 1):
                    if i%2 == 0:
                        genomes_list[aibots_list.index(aibot)].fitness += 5
                    else:
                        genomes_list[aibots_list.index(aibot)].fitness -= 5
                score_left_bool = False

            if score_right_bool:
                score_right += 1 # right team scores a goal
                for i, aibot in enumerate(aibots_list, 1):
                    if i%2 != 0:
                        genomes_list[aibots_list.index(aibot)].fitness += 5
                    else:
                        genomes_list[aibots_list.index(aibot)].fitness -= 5
                score_right_bool = False

            for obstacle in obstacles_list:
                obstacle.x, obstacle.y = (world.width/2, world.height/2)
                obstacle.angle = 0
                obstacle.speed = 0

            for i, aibot in enumerate(aibots_list, 1):
                aibot.x = 100 + (world.width - 200)*(genome_id%2)
                aibot.y = world.height/2
                aibot.angle = 0
                aibot.speed = 0

        # if no score, punish them every second
        elif time_s >= 1.0:
            for aibot in aibots_list:
                genomes_list[aibots_list.index(aibot)].fitness -= 1

        # Draw Obstacles
        for obstacle in obstacles_list:
            pygame.draw.circle(game_window.screen, obstacle.color,
                               (obstacle.x, obstacle.y), obstacle.size)

        # Draw AIBots
        for aibot in aibots_list:
            pygame.draw.circle(game_window.screen, aibot.color,
                               (aibot.x, aibot.y), aibot.size)
        
        # Draw gorillas (at left and right of the screen and vertically centered)
        # game_window.screen.blit(gorilla_left.image, (0, world.height/2 - gorilla_left.height/2))
        # game_window.screen.blit(gorilla_right.image, (world.width - gorilla_right.width, world.height/2 - gorilla_right.height/2))

        # Draw text
        # Time
        draw_text(f"Timer: {int(timer)}", becode_color,
                  (game_window.width_px - 100, 50))

        # current generations
        draw_text(f"Generation: {generation}",
                  becode_color, (game_window.width_px/2, 50))

        # Number of AIBots alive
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
    1. Create population of AIBots. Each AIBots has its own neural network.
    2. Run the game for that population and set their respective fitness scores based on how long they survive.
    """
    # Global
    global generation
    generation += 1  # Increment by 1 at every game session

    # Variables
    game_running: bool = True  # Game loop
    time_s: float = 0.0
    # current_level_index = 1 # level 1
    player_1.x, player_1.y = (100, world.height/2)  # Restart player position

    # Create empty lists
    genomes_list: list = []
    aibots_list: List[AIBots] = []
    neural_nets_list: list = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # AIBot starts the game with fitness score at 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets_list.append(net)
        # create an aibot with specific size and starting at random y position within boundaries included
        aibot_size = 100
        # aibot_y = random.uniform(aibot_size, world.height - aibot_size)
        aibot_y = world.height/2
        aibots_list.append(
            AIBots((world.width - 100, aibot_y), size=aibot_size, mass=50))
        genomes_list.append(genome)

    # Instantiate aibots
    # aibot_1 = AIBots((world.width - 100, world.height/2), size=50, mass=1)

    # Enter game loop
    while game_running and len(aibots_list):

        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get user input
        user_input = client_1.get_user_input()

        # Go to next generation if player press return button
        if isinstance(user_input, str):
            # game_running = False
            break

        # Display background
        # Display level 1 background surface
        # blit() to display a surface on another surface: here to display level surface on screen
        # (0,0): the position of the top left of bg_surface
        # if user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
            world.width, world.height = user_input  # update the environment as well
        game_window.screen.fill(world.color)  # fill the screen with white
        # game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, (game_window.width_px,game_window.height_px)), (0,0))
        # game_window.screen.blit(levels_list[current_level_index].bg_surface, (0,0))

        # Reward each AIBot a fitness of 0.1 for each frame it stays alive
        for i, aibot in enumerate(aibots_list):
            genomes_list[i].fitness += 0.1

        # get_ai_decision()
        # Give its location and its distance compared to player => neural network will output a list of values
        # From which it can determine in which direction to move
        # Use a tanh activation function to have the output results between -1 and 1
            # output: list = neural_nets_list[i].activate((aibot.x, aibot.y, abs(
            #     aibot.x - client_1.player.x), abs(aibot.y - client_1.player.y)))
            
            # As input: its location and its distance compared to player and other bots
            # distance_between_bots = []
            # for j, other_aibot in enumerate(aibots_list):
            #     if i != j:
            #         distance_between_bots.extend([abs(aibot.x - other_aibot.x), abs(aibot.y - other_aibot.y)])
            
            # input_list: list = [aibot.x,
            #     aibot.y,
            #     abs(aibot.x - client_1.player.x),
            #     abs(aibot.y - client_1.player.y)
            #     ]
            # input_list.extend(distance_between_bots)
            # # print(len(input_list)) # should be 4 + (2*99) = 200
            # output: list = neural_nets_list[i].activate(input_list)

            # As input: its location and its distance compared to player and obstacles
            distances_to_obstacles = []
            for obstacle in obstacles_list:
                distances_to_obstacles.extend([abs(aibot.x - obstacle.x), abs(aibot.y - obstacle.y)])
            
            input_list: list = [aibot.x,
                aibot.y,
                abs(aibot.x - client_1.player.x),
                abs(aibot.y - client_1.player.y)
                ]
            input_list.extend(distances_to_obstacles)
            # print(len(input_list)) # should be 4 + (2*30)
            output: list = neural_nets_list[i].activate(input_list)

            # if output[0] > 0.5: go left
            if output[0] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (- 1 * math.pi/2, 2))
            if output[1] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi/2, 2))
            if output[2] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (0, 2))
            if output[3] > 0.5:
                aibot.angle, aibot.speed = world.add_vectors(
                    (aibot.angle, aibot.speed), (math.pi, 2))

            # Limits aibot's speed
            if aibot.speed > 20:
                aibot.speed = 20

            aibot.move()
            world.add_air_resistance(aibot)
            world.attraction(player_1, aibot)
            world.bounce(aibot)
            # bounce: bool = world.bounce(aibot)
            # If hits a border, punish the aibot to prevent him from just staying at the border
            # if bounce:
            #     genomes_list[i].fitness -= 3

            collide_player: bool = world.collide(player_1, aibot, True)
            # If collision, reward the aibot
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
            
            # for other_aibot in aibots_list[i+1:len(aibots_list) - 1]:
            #     collide_otherbot: bool = world.collide(aibot, other_aibot, True)
            #     if collide_otherbot:
            #         genomes_list[aibots_list.index(aibot)].fitness -= 3
            #         genomes_list[aibots_list.index(other_aibot)].fitness -= 3

            # If collision, punish the aibot and remove it
            # if collide_player:
            #     genomes_list[aibots_list.index(aibot)].fitness -= 5
            #     neural_nets_list.pop(aibots_list.index(aibot))
            #     genomes_list.pop(aibots_list.index(aibot))
            #     aibots_list.pop(aibots_list.index(aibot))

        player_1.move()
        world.add_air_resistance(player_1)
        world.bounce(player_1)

        for obstacle in obstacles_list:
            obstacle.move()
            world.add_air_resistance(obstacle)
            world.collide(obstacle, player_1, True)
            world.bounce(obstacle)
            # Limits obstacle's speed
            if obstacle.speed > 20:
                obstacle.speed = 20

            
        # Draw Obstacles
        for obstacle in obstacles_list:
            pygame.draw.circle(game_window.screen, obstacle.color,
                               (obstacle.x, obstacle.y), obstacle.size)

        # Draw Players
        pygame.draw.circle(game_window.screen, player_1.color,
                           (player_1.x, player_1.y), player_1.size)

        # Draw AIBots
        for aibot in aibots_list:
            pygame.draw.circle(game_window.screen, aibot.color,
                               (aibot.x, aibot.y), aibot.size)

        # Draw text
        # Time
        draw_text(f"Time: {int(time_s)}", becode_color,
                  (game_window.width_px - 100, 50))

        # current generations
        draw_text(f"Generation: {generation}",
                  becode_color, (game_window.width_px/2, 50))

        # Number of AIBots alive
        draw_text(f"Alive: {len(aibots_list)}",
                  becode_color, (game_window.width_px/2, 100))

        # Update the screen with the drawings
        pygame.display.update()
        # pygame.display.flip() # difference between flip() and update(): flip updates the entire screen; update(rect) you can update portion of the display

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
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))  # DD: this gets some stats
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(game, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

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

    # Instantiate obstacles
    # obstacles_list: List[Obstacle] = []
    # min_size: int = 30
    # max_size: int = 30
    # for _ in range(3):
    #     obstacle = Obstacle((random.uniform(0, world.width), random.uniform(
    #         0, world.height)), size=random.uniform(min_size, max_size), mass=50)
    #     obstacles_list.append(obstacle)

    # Instantiate gorilla
    gorilla = Gorilla((game_window.width_px, game_window.height_px))
    gorilla.image = pygame.image.load("gamecore/assets/images/gorilla.png").convert_alpha()
    gorilla.image_flip = pygame.transform.flip(gorilla.image, True, False)
    
    # import gorilla sounds
    gorilla.sounds = pygame.mixer.Sound(
        "gamecore/assets/sounds/gorilla_sounds.mp3")

    # Start screen: Title slide and dialogue with gorilla
    level_0 = create_level("Title", "slide", "gamecore/assets/images/title_slide.png", bg_color=becode_color, font_color= (255,255,255), resize=True)
    start_screen(level_0)

    # # Start game_1
    # level_1 = create_level("Level 1", "game_level", bg_color=(255,255,255))
    # config_path = "gamecore/config-feedforward.txt"
    # run(config_path, game_1)

    # # Start game_2
    # level_2 = create_level("Level 1", "game_level", bg_color=(255,255,255))
    # config_path = "gamecore/config-feedforward-2.txt"
    # run(config_path, game_2)

    # # Start game_3
    # level_3 = create_level("Level 1", "game_level", bg_color=(120,184,51))
    # config_path = "gamecore/config-feedforward-3.txt"
    # run(config_path, game_3)

    # Quit the program
    terminate()
