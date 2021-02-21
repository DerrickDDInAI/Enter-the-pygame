"""
Main script that executes the game
"""
#=====================================================================
# Import
#=====================================================================

import pygame
from pygame.color import THECOLORS
import sys

## Import local modules
import player
import level


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
        Function that creates an instance of GameWindow class
        By default:
        * caption is "game" if no caption is provided
        """
        self.caption = caption
        self.width_px, self.height_px = window_dimensions_px

        # Create a display surface called screen by convention
        self.screen = pygame.display.set_mode((self.width_px, self.height_px))

    def display_caption(self):
        """
        Function to display the caption
        """
        pygame.display.set_caption(self.caption)



#============================================================
# Main functions
#============================================================

def terminate():
    """
    Function that quit the game and terminate the script.
    """
    pygame.quit()
    sys.exit()

def main():

    # Globals
    global game_window

    # CONSTANTS
    WINDOW_WIDTH_PX = 1440
    WINDOW_HEIGHT_PX = 780
    CAPTION = "Enter the Pygame"

    # Setup
    pygame.init() # initiate pygame
    pygame.font.init()  # initiate font
    # game_font = pygame.font.Font('04B_19.ttf',40) # create a font (style, size)
    game_font = pygame.font.SysFont("comicsans", 50)
    # END_FONT = pygame.font.SysFont("comicsans", 70)

    game_window = GameWindow((WINDOW_WIDTH_PX, WINDOW_HEIGHT_PX), CAPTION)
    game_window.display_caption() 
    main_clock = pygame.time.Clock() # instantiate clock to limit the frame rate

    # Variables
    running = True # game loop 
    framerate_limit = 120
    time_s = 0.0


    while running:
        # Get the delta t for one frame (this changes depending on system load).
        dt_s = float(main_clock.tick(framerate_limit) * 1e-3)

        # Get each user input
        for event in pygame.event.get():

            # Quit the game if you click on the X button at the top of the screen
            if event.type == pygame.QUIT:
                running = False
                break

            # Quit the game if you release the escape button
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Fill the window with BeCode color
        game_window.screen.fill((22,35,46))
        # game_window.screen.fill(THECOLORS['black'])

        # Update the screen with the drawings
        pygame.display.update()
        
        # Time
        time_s += dt_s # Measure time spent
        main_clock.tick(framerate_limit) # Limit the frame rate to max the framerate_limit


#============================================================
# Run
#============================================================

main()
terminate()