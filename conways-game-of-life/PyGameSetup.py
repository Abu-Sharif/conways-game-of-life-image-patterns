import time

import pygame
from BMPImage import read_bmp, initialize_grid_from_the_image, update_grid, count

# This is the max window size
max_image_height = 800
max_image_width = 800
border_color = (40, 40, 40) # Grey cell-border used in the display grid

# Uses grid representation of alive/dead cells along with their respective colors and converts it to a PyGame representation
def display_image_grid(grid, color_grid, dominant_colors, time_between_new_generation):
    pygame.init()
    counter = 0
    # Grab the height and width from the grid
    height = len(grid)
    width = len(grid[0])

    # scale the image to fit the screen
    scale_factor = min(max_image_width // width, max_image_height // height)
    cell_size = max(1, scale_factor) # Make each cell a multiple, otherwise the cell's will be tiny

    # Set display window size based on scaled cells
    window_width = width * cell_size
    window_height = height * cell_size

    screen = pygame.display.set_mode((window_width, window_height)) # grid width, width * (cell size)
    pygame.display.set_caption("Conway's Game of Life - Abu Sharif") # Title for the screen

    clock = pygame.time.Clock()
    running = True
    last_updateed_time = pygame.time.get_ticks() # keep track of time

    while (running == True): # While PyGame grid is running

        # If user exits the window or presses the ESC on their keyboard, exit PyGame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        current_time = pygame.time.get_ticks()
        if current_time - last_updateed_time >= time_between_new_generation: #time to update grid
            grid, color_grid = update_grid(grid, color_grid, dominant_colors) # update grid cells and colors
            last_updateed_time = current_time
            counter += 1
            print("Generation : #" ,counter)

        screen.fill(border_color)

        # iterate over the grid
        for y in range(height):
            for x in range(width):

                if grid[y][x] == 1: # if the cell is alive, value is 1, other it is dead and value is 0
                    color, dont_need_this_var  = color_grid[y][x] # alive cell
                else:
                    color, dont_need_this_var  = color_grid[y][x] # dead cell

                # In order for the grid borders to be visible, I've indented the pixel inside the cell
                # This leaves a small 1 pixel border on each side of the pixel which is used to create the grey-border grid
                rect = pygame.Rect(
                    x * cell_size + 1,
                    y * cell_size + 1,
                    cell_size - 2,
                    cell_size - 2
                )
                pygame.draw.rect(screen, color, rect) # initializing that blank square to it's corresponding pixel value=

        pygame.display.flip() # This will refresh the display as squares are updated
        clock.tick(60)
    pygame.quit()




