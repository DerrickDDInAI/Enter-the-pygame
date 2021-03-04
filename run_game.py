"""
Game to demonstrate how:
- to write a game with python and pygame;
- to implement an AI model to solve the game by using neat module.
"""
#=====================================================================
# Import
#=====================================================================

## Import internal modules
import sys
# import os.path
import math
from typing import List, Set, Dict, TypedDict, Tuple, Optional

## Import 3rd party modules
import pygame
from pygame.color import THECOLORS


## Import local modules
from gamecore.level import Level
from gamecore.environment import Environment
from gamecore.player import AIBots, Player, Gorilla



#=====================================================================
# Classes
#=====================================================================

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
        self.screen = pygame.display.set_mode((self.width_px, self.height_px), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

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
    
    def get_user_input(self) -> dict:
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
                if event.key == pygame.K_SPACE: # and player.boost == 5.0:
                    pass

            # Check keys continuously pressed
            keys = pygame.key.get_pressed()
            if keys:
                keys_pressed = {"left": False, "right": False, "up": False, "down": False}
                if keys[pygame.K_LEFT]:
                    keys_pressed["left"] = True
                if keys[pygame.K_RIGHT]:
                    keys_pressed["right"] = True
                if keys[pygame.K_UP]:
                    keys_pressed["up"] = True
                if keys[pygame.K_DOWN]:
                    keys_pressed["down"] = True
                return keys_pressed
            # Resize the display
            if event.type == pygame.VIDEORESIZE:
                game_window.screen = pygame.display.set_mode(
                    event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                return event.dict['size']
                # game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, event.dict['size']), (0,0))
                # pygame.display.flip()
    
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
#============================================================
# Main functions
#============================================================
def create_levels() -> List:
    """
    Function to create the levels.

    Return: list of levels
    """
    
    # 1. Create Level instances
    title_slide = Level("Title", "slide", "gamecore/assets/images/title_slide.png")
    level_1 = Level("A new dimension")

    # 2. Import the background image
    ## convert() is not necessary but converts the image into a format easier for pygame => faster
    title_slide.bg_surface = pygame.image.load(title_slide.bg_surface_path).convert()

    ## 3. If necessary, resize the background image
    title_slide.bg_surface = pygame.transform.scale(title_slide.bg_surface, (game_window.width_px,game_window.height_px))

    return Level.levels_list

def terminate() -> None:
    """
    Function to quit the game and terminate the script.
    """
    pygame.quit()
    sys.exit()

def get_ai_decision():
    pass

def draw_text(text: str, xy_pos_center: Tuple[int,int]):
    """
    Function to display text
    * param 
    :text to display
    :xy_pos_center (x,y) coordinates of the center of text rectangle
    
    """
    text_surface = game_font.render(text, True, (255,255,255)) # text, True for anti-aliased text, color in rgb
    text_rect = text_surface.get_rect(center=xy_pos_center) # put the text in a rect to make it easier to display
    game_window.screen.blit(text_surface, text_rect)


def main() -> None:

    # Globals
    global game_window, game_font

    # CONSTANTS
    WINDOW_WIDTH_PX = 1440
    WINDOW_HEIGHT_PX = 900
    CAPTION = "Enter the Pygame"

    # Setup
    pygame.init() # initiate pygame
    pygame.font.init()  # initiate font
    # game_font = pygame.font.Font('04B_19.ttf',40) # create a font (style, size)
    game_font = pygame.font.SysFont("comicsans", 50)
    # END_FONT = pygame.font.SysFont("comicsans", 70)

    # Display
    game_window = GameWindow((WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX), CAPTION)
    game_window.display_caption()

    # Clock
    main_clock = pygame.time.Clock() # instantiate clock to limit the frame rate

    # Variables
    start_screen = True # start screen loop
    game_running = True # game loop 
    framerate_limit = 120
    time_s = 0.0
    current_level_index = 0
    current_start_event = -1 # events happen at the start screen (event -1: just title slide; event 1: gorilla appears; event 2,3,...: dialogue; last event: gorilla disappears and game starts)
    # # Create empty dictionary that will store user input when necessary
    # input_dict: dict = {"size": None, "level": 0} 

    # Instantiate environment
    world = Environment((WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX), color=(255,255,255))
    # Instantiate player
    # player_1 = Player(20, (1,1),'Yoyo', (255,0,0))
    player_1 = Player((100, world.height/2), size=50, mass=100, name="John Titor", color=(22,35,46))

    # Instantiate local client who will control player_1
    client_1 = Client(player_1)

    # Instantiate aibots
    aibot_1 = AIBots((world.width - 100, world.height/2), size=50, mass=200)

    # Instantiate gorilla
    gorilla = Gorilla("gamecore/assets/images/gorilla.png", (game_window.width_px,game_window.height_px))
    ## convert() converts the image into a format easier for pygame => faster
    ## alpha() otherwise pygame paints black where the image is empty/transparent
    gorilla.image = pygame.image.load(gorilla.image_path).convert_alpha()
    gorilla.image_flip = pygame.image.load(gorilla.image_path).convert_alpha()
    gorilla.image_flip = pygame.transform.flip(gorilla.image, True, False) # flip the gorilla horizontally

    
    # Start screen
    levels_list = create_levels()
    while start_screen:

        user_input = client_1.wait_for_pressed_key()
        # if user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input,tuple):
            game_window.width_px, game_window.height_px = user_input
        game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, (game_window.width_px,game_window.height_px)), (0,0))

        # if user_input is True, it means the user pressed a key
        if user_input == True:
            current_start_event += 1

        # 1. Big text appears
        # if current_start_event == 1:
        #     game_window.screen.fill((22,35,46)) # fill the screen with BeCode color
        #     draw_text(str(round(time_s, 2)), (game_window.width_px/2,game_window.height_px - 20))
        #     if time_s >= 5 and current_dialogue_index < 2:
        #         time_s = 0.0 # reset time
        #         current_dialogue_index += 1
        #     draw_text(gorilla.dialogues[current_dialogue_index], (game_window.width_px/2,game_window.height_px/2))

        # 1. Big text appears
        if current_start_event in [0,1,2]:
            game_window.screen.fill((22,35,46)) # fill the screen with BeCode color
            draw_text(gorilla.dialogues[current_start_event], (game_window.width_px/2,game_window.height_px/2))
        
        # 2. Gorilla appears from the right of the screen
        elif current_start_event == 3:
            game_window.screen.fill((22,35,46)) # fill the screen with BeCode color
            gorilla.move()
            game_window.screen.blit(gorilla.image, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
        
        # 3. Gorilla speaks
        elif current_start_event in [4,5,6,7]:
            game_window.screen.fill((22,35,46)) # fill the screen with BeCode color
            draw_text(gorilla.dialogues[current_start_event], (game_window.width_px/2,game_window.height_px/2))
            game_window.screen.blit(gorilla.image, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))

        # 4. Gorilla turns its back and speaks
        elif current_start_event in [8,9]:
            game_window.screen.fill((22,35,46)) # fill the screen with BeCode color
            draw_text(gorilla.dialogues[current_start_event], (game_window.width_px/2,game_window.height_px/2))
            game_window.screen.blit(gorilla.image_flip, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
        
        # 5. Gorilla faces towards left again and speaks
        elif current_start_event in [10,11,12,13]:
            game_window.screen.fill((22,35,46)) # fill the screen with BeCode color
            draw_text(gorilla.dialogues[current_start_event], (game_window.width_px/2,game_window.height_px/2))
            game_window.screen.blit(gorilla.image, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
        
        # 6. Gorilla turn its back and leaves the screen from the right
        elif current_start_event == 13:
            game_window.screen.fill((255,255,255)) # fill the screen with white
            gorilla.move()
            game_window.screen.blit(gorilla.image_flip, (gorilla.x - gorilla.image.get_width(), gorilla.y - gorilla.image.get_height() - 100))
        
        # Quit the start screen loop
        elif current_start_event == 14:
            start_screen = False

        # Update the screen with the drawings
        pygame.display.update()

    ## Fill the window with BeCode color
    # game_window.screen.fill((22,35,46))
    # game_window.screen.fill(THECOLORS['black'])
    # pygame.display.update()

    # Enter level 1
    current_level_index = 1

    while game_running:
        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get user input
        user_input = client_1.get_user_input()
        get_ai_decision()
        
        # Display background
        ## Display level 1 background surface
        ## blit() to display a surface on another surface: here to display level surface on screen
        ## (0,0): the position of the top left of bg_surface
        # if user_input is a tuple, it means the user changed the screen size
        if isinstance(user_input,tuple):
            game_window.width_px, game_window.height_px = user_input
        game_window.screen.fill(world.color) # fill the screen with white
        # game_window.screen.blit(pygame.transform.scale(levels_list[current_level_index].bg_surface, (game_window.width_px,game_window.height_px)), (0,0))
        # game_window.screen.blit(levels_list[current_level_index].bg_surface, (0,0)) 

        # if user_input is a dictionary, it means the user is pressing a key
        if isinstance(user_input,dict):
            if user_input["left"]:
                player_1.angle -= 1
            if user_input["right"]:
                player_1.angle += 1
            if user_input["up"]:
                player_1.angle = math.pi - player_1.angle
            if user_input["down"]:
                player_1.angle = math.pi + player_1.angle
            player_1.speed *= 2
        
        player_1.move()
        world.attraction(player_1, aibot_1)
        world.add_air_resistance(player_1)
        world.collide(player_1, aibot_1)
        world.bounce(player_1)

        # Players
        pygame.draw.circle(game_window.screen, player_1.color, (player_1.x, player_1.y), player_1.size)

        # AIBots
        pygame.draw.circle(game_window.screen, aibot_1.color, (aibot_1.x, aibot_1.y), aibot_1.size)


        # Update the screen with the drawings
        pygame.display.update()
        # pygame.display.flip() # difference between flip() and update(): flip updates the entire screen; update(rect) you can update portion of the display
        
        # Time
        time_s += dt_s # Measure time spent
        main_clock.tick(framerate_limit) # Limit the frame rate to max the framerate_limit


#============================================================
# Run
#============================================================

main()
terminate()