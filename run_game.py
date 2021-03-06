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
# import os.path
import math
from typing import List, Set, Dict, TypedDict, Tuple, Optional

# Import 3rd party modules
import pygame
# from pygame.color import THECOLORS
import neat

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


def create_levels() -> List:
    """
    Function to create the levels.

    Return: list of levels
    """

    # 1. Create Level instances
    title_slide = Level(
        "Title", "slide", "gamecore/assets/images/title_slide.png")
    level_1 = Level("A new dimension")

    # 2. Import the background image
    # convert() is not necessary but converts the image into a format easier for pygame => faster
    title_slide.bg_surface = pygame.image.load(
        title_slide.bg_surface_path).convert()

    # 3. If necessary, resize the background image
    title_slide.bg_surface = pygame.transform.scale(
        title_slide.bg_surface, (game_window.width_px, game_window.height_px))

    return Level.levels_list


def terminate() -> None:
    """
    Function to quit the game and terminate the script.
    """
    pygame.quit()
    sys.exit()


def get_ai_decision():
    pass


def draw_text(text: str, color: Tuple[int, int, int], xy_pos_center: Tuple[int, int]):
    """
    Function to display text
    * param 
    :text :text to display
    :color :font color
    :xy_pos_center (x,y) coordinates of the center of text rectangle

    """
    text_surface = game_font.render(
        text, True, color)  # text, True for anti-aliased text, color in rgb
    # put the text in a rect to make it easier to display
    text_rect = text_surface.get_rect(center=xy_pos_center)
    game_window.screen.blit(text_surface, text_rect)


def start_screen() -> None:
    """
    Function to start at level 0: "Title slide"
    """
    # Variables
    start_screen = True
    time_s: float = 0.0
    current_level_index = 0
    current_story_event = -1  # title slide just before gorilla speaks
    transition_color = list(becode_color) # to turn the screen whiter every second

    while start_screen:
        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)
        
        # Get user input
        user_input = client_1.wait_for_pressed_key()

        # If user_input is a tuple, the user changed the screen size
        if isinstance(user_input, tuple):
            game_window.width_px, game_window.height_px = user_input
        game_window.screen.blit(pygame.transform.scale(
            levels_list[current_level_index].bg_surface, (game_window.width_px, game_window.height_px)), (0, 0))

        # If user_input is True, the user pressed a key to go forward in the story
        if user_input == True:
            current_story_event += 1

        # 1. Big text appears
        # if current_start_event == 1:
        #     game_window.screen.fill(becode_color) # fill the screen with BeCode color
        #     draw_text(str(round(time_s, 2)), (game_window.width_px/2,game_window.height_px - 20))
        #     if time_s >= 5 and current_dialogue_index < 2:
        #         time_s = 0.0 # reset time
        #         current_dialogue_index += 1
        #     draw_text(gorilla.dialogues[current_dialogue_index], (game_window.width_px/2,game_window.height_px/2))

        # 1. Big text appears
        if current_story_event in [0, 1, 2]:
            # fill the screen with BeCode color
            game_window.screen.fill(becode_color)
            draw_text(gorilla.dialogues[current_story_event], slide_font_color, (
                game_window.width_px/2, game_window.height_px/2))
            gorilla.sounds.play()

        # 2. Gorilla appears from the right of the screen
        elif current_story_event == 3:
            # fill the screen with BeCode color
            game_window.screen.fill(becode_color)
            gorilla.move()
            game_window.screen.blit(
                gorilla.image, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
            gorilla.sounds.play()

        # 3. Gorilla speaks
        elif current_story_event in [4, 5, 6, 7]:
            # fill the screen with BeCode color
            game_window.screen.fill(becode_color)
            draw_text(gorilla.dialogues[current_story_event], slide_font_color, (
                game_window.width_px/2, game_window.height_px/2))
            game_window.screen.blit(
                gorilla.image, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
            gorilla.sounds.play()

        # 4. Gorilla turns its back and speaks
        elif current_story_event in [8, 9]:
            # fill the screen with BeCode color
            game_window.screen.fill(becode_color)
            draw_text(gorilla.dialogues[current_story_event], slide_font_color, (
                game_window.width_px/2, game_window.height_px/2))
            game_window.screen.blit(gorilla.image_flip, (
                gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
            gorilla.sounds.play()

        # 5. Gorilla faces towards left again and speaks
        elif current_story_event in [10, 11, 12, 13]:
            # fill the screen with BeCode color
            game_window.screen.fill(becode_color)
            draw_text(gorilla.dialogues[current_story_event], slide_font_color, (
                game_window.width_px/2, game_window.height_px/2))
            game_window.screen.blit(
                gorilla.image, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
            gorilla.sounds.play()

        # 6. Gorilla turn its back and leaves the screen from the right
        elif current_story_event == 13:
            game_window.screen.fill(becode_color)
            gorilla.move()
            game_window.screen.blit(gorilla.image_flip, (
                gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
            gorilla.sounds.play()

        # Transition before quitting the start screen loop
        elif current_story_event == 14:
            
            # Turn the screen whiter every second
            if time_s > 0.001:
                for i, color in enumerate(transition_color):
                    if transition_color[i] < 255:
                        transition_color[i] += 1
                time_s = 0.0 # reset timer
            game_window.screen.fill(transition_color)
        
        # Quit the start screen loop
        elif current_story_event == 15:
            # stop gorilla sounds
            gorilla.sounds.stop()
            start_screen = False

        # Update the screen with the drawings
        pygame.display.update()

        # Time
        time_s += dt_s  # Measure time spent
        # Limit the frame rate to max the framerate_limit
        main_clock.tick(framerate_limit)


def game(genomes, config) -> None:
    """
    Function to play the game for current genome of AIBots.
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
        aibot_size = 10
        # aibot_y = random.uniform(aibot_size, world.height - aibot_size)
        aibot_y = world.height/2
        aibots_list.append(
            AIBots((world.width - 100, aibot_y), size=aibot_size, mass=50))
        genomes_list.append(genome)

    print(aibots_list[0].speed)

    # Instantiate aibots
    # aibot_1 = AIBots((world.width - 100, world.height/2), size=50, mass=1)

    # Enter game loop
    while game_running and len(aibots_list):

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


def run(config_file):
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
    # global game_window, game_font, player_1, world
    # global generation

    # CONSTANTS
    WINDOW_WIDTH_PX = 1440
    WINDOW_HEIGHT_PX = 900
    CAPTION = "Enter the Pygame"

    # Variables
    framerate_limit = 120
    generation = 0
    slide_font_color = (255, 255, 255)
    becode_color = (22, 35, 46)

    # Setup
    pygame.init()  # initiate pygame
    pygame.font.init()  # initiate font
    game_font = pygame.font.SysFont("comicsans", 50)
    # end_font = pygame.font.SysFont("comicsans", 70)
    # game_font = pygame.font.Font('04B_19.ttf',40) # create a font (style, size)

    # Display
    game_window = GameWindow((WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX), CAPTION)
    game_window.display_caption()

    # Clock
    main_clock = pygame.time.Clock()  # instantiate clock to limit the frame rate

    # Instantiate environment
    world = Environment((WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX),
                        color=(255, 255, 255))
    # Instantiate player
    # player_1 = Player(20, (1,1),'Yoyo', (255,0,0))
    player_1 = Player((100, world.height/2), size=20, mass=100,
                      name="John Titor", color=becode_color)

    # Instantiate local client who will control player_1
    client_1 = Client(player_1)

    # Instantiate obstacles
    obstacles_list: List[Obstacle] = []
    min_size: int = 10
    max_size: int = 20
    for _ in range(30):
        obstacle = Obstacle((random.uniform(0, world.width), random.uniform(
            0, world.height)), size=random.uniform(min_size, max_size), mass=50)
        # Assign rectangle: pygame.Rect(left, top, width, height)
        # obstacle.rect = pygame.Rect(obstacle.x, obstacle.y, random.uniform(obstacle_min_size, world.width/10), random.uniform(obstacle_min_size, world.width/10))
        obstacles_list.append(obstacle)

    # Instantiate gorilla
    gorilla = Gorilla("gamecore/assets/images/gorilla.png",
                      (game_window.width_px, game_window.height_px))
    # convert() converts the image into a format easier for pygame => faster
    # alpha() otherwise pygame paints black where the image is empty/transparent
    gorilla.image = pygame.image.load(gorilla.image_path).convert_alpha()
    gorilla.image_flip = pygame.image.load(gorilla.image_path).convert_alpha()
    gorilla.image_flip = pygame.transform.flip(
        gorilla.image, True, False)  # flip the gorilla horizontally
    # import gorilla sounds
    gorilla.sounds = pygame.mixer.Sound(
        "gamecore/assets/sounds/gorilla_sounds.mp3")

    # Create levels
    levels_list = create_levels()

    # Start screen
    # start_screen()

    # Start game
    config_path = "gamecore/config-feedforward.txt"
    run(config_path)
    terminate()
