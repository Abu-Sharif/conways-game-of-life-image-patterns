import random
from Color import get_dominant_color

#
def read_bmp(file_path):
    with open(file_path, 'rb') as f:
        # Read BMP Header which is 54 bytes total length
        header = f.read(54) # Width, height, pixel_offset is gathered from BMP File header
        width = int.from_bytes(header[18:22], 'little')  # Image width
        height = int.from_bytes(header[22:26], 'little')  # Image height
        pixel_offset = int.from_bytes(header[10:14], 'little')  # Pixel data offset

        # Move to pixel data
        f.seek(pixel_offset)

        # Each row is padded to a multiple of 4 bytes
        row_padding = (4 - (width * 3) % 4) % 4

        pixels = []  # Store the pixel data we grabbed into this list

        for y in range(height):
            row = []
            for x in range(width):
                # Read BGR (Blue, Green, Red) values
                blue = int.from_bytes(f.read(1), 'little')
                green = int.from_bytes(f.read(1), 'little')
                red = int.from_bytes(f.read(1), 'little')

                # Store as RGB tuple
                row.append((red, green, blue))

            # Skip padding bytes
            f.read(row_padding)

            # Insert row at the beginning because BMP is bottom-up
            pixels.insert(0, row)

    return pixels, width, height



# Standard luminance formula, will be used to determine alive/dead states of cells
def get_brightness(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

# Creating the initial grid, by associating cell-states and color-values to each pixel
def initialize_grid_from_the_image(pixels):

    # Using the image, initialize the height, width, and starting cell configuration
    original_image_height = len(pixels) # Height of the original image
    original_image_width = len(pixels[0]) # Width of the original image

    # To maintain comparison of all grids, use fix sized grid dimensions & scale image to fit within it
    height_required = 100
    width_required = 100
    scale_height = original_image_height / height_required
    scale_width = original_image_width / width_required

    # My choice of what brightness/RGB values will define if a cell alive or dead
    brightness_threshold_level = 128

    # Grids Lists:
    grid = [] # Stores each cell's state (alive/dead)
    color_grid = [] # Stores the RGB colors of each cell

    # Grab the dominant colors that are present in the image
    dominant_colors = get_dominant_color(pixels, 5)


    # Iterate over each pixel add a cell state, and it's color into their respective lists. This will create the first grid
    for y in range(height_required): # columns of the grid
        row = []
        color_row = []
        for x in range(width_required): # rows in the grid

            # grab the pixel that corresponds to the row & column, i.e the cell location
            # Technically the grid & cells haven't been created yet, hence variable names refer "pixel" and not "cell"
            pixel_y= int(y * scale_height)
            pixel_x = int(x * scale_width)

            # grab the color of the current pixel - i.e the cell, and calculate each pixel's brightness level
            pixel_color = pixels[pixel_y][pixel_x]
            pixel_brightness = get_brightness(pixels[pixel_y][pixel_x])

            # Depending on pixel's brightness relative to threshold amount we consider it alive or dead & initialize its state accordingly (1 or 0)
            if (pixel_brightness >= brightness_threshold_level):
                cell_state = 0
                row.append(cell_state)
                color_row.append((pixel_color, 0)) # cell is dead - keeps current color - fade initialized to 0 (will increase over time)
            else:
                cell_state = 1
                row.append(cell_state)
                color_row.append((random.choice(dominant_colors), 0)) # cell is alive - we chose a new dominant color for it


        grid.append(row)
        color_grid.append(color_row)

    # Return the state-grid, and color-grid with now initialized cells
    return grid, color_grid, dominant_colors
count  = 0

# Update state-grid and color-grid for the next generation, create a new grid (if we alter original grids, it will affect generation)
def update_grid(grid, color_grid, dominant_colors):

    height = len(grid)
    width = len(grid[0])

    # Grid will store cell-states of the next grid generation
    new_updated_grid = []
    new_color_grid = [] # Update the color-grid every generation or cells will not change colors (including newly alive ones)

    # Iterate over each cell in grid
    for current_cell_y in range(height):

        new_row = [] # Will hold the state of each cell in the next generation
        new_color_row = [] # Will hold the color of each cell in the next generation

        for current_cell_x in range(width):

            # The amount of alive neighbors that the current cell has (within 3x3 radius of it)
            current_alive_neighbors = 0
            color, fade_count = color_grid[current_cell_y][current_cell_x]

            # Grab a 3x3 neighbor grid of the current cell, each cells needs to know state of cells within a 3x3 of it
            for neighbor_height_y in range(current_cell_y - 1, current_cell_y + 2): # y-coordinates of grid
                for neighbor_width in range(current_cell_x -1, current_cell_x + 2): # x-coordinates of the grid

                    #Skip over the cell itself since we only care about the state of it's neighbor
                    if neighbor_height_y == current_cell_y and neighbor_width == current_cell_x:
                        continue

                    # Check to ensure neighbor is within the grid
                    if (0 <= neighbor_height_y < height and 0 <= neighbor_width < width):

                        # add an alive neighbor if there is a cell alive within the current cell's 3x3 sub-grid
                        if (grid[neighbor_height_y][neighbor_width] == 1):
                            current_alive_neighbors += 1

            # Rules for color fading
            fade_decay_rate = 0.10 # fade by 10% per generation
            min_brightness_factor = .97

            # Applying the rules of the Game of Life:
            if grid[current_cell_y][current_cell_x] == 1: # If the current cell is alive

                # If there are 2 or 3 alive neighboring cells, then current cell stays alive in next generation
                if (current_alive_neighbors == 2 or current_alive_neighbors == 3):
                    new_row.append(1)
                    new_color_row.append((color, 0)) # maintains color. fade stays at 0

                # Too many or too little neighboring cells remain alive, current cell will die next generation
                else:
                    new_row.append(0)
                    fade_count += 1 # increase the fade_count each generation it stays dead

                    # list to store the color values
                    faded_color_list = []

                    for c in color: # loop through each color in the RGB tuple

                        # Calculate the faded value here
                        faded_value = int(c * (fade_decay_rate * fade_count))

                        # calculate the minimum fade value based on the original color, and append to the list
                        min_allowed_value = int(c * min_brightness_factor)
                        final_value = max(faded_value, min_allowed_value)
                        faded_color_list.append(final_value)

                    # Convert the list of colors into a tuple, store color and fade_count for next gen
                    faded_color = tuple(faded_color_list)
                    new_color_row.append((faded_color, fade_count))


            # If the current cell is dead, and has 3 live neighbors, it becomes alive in next generation
            if grid[current_cell_y][current_cell_x] == 0:
                if(current_alive_neighbors == 3):
                    new_row.append(1)
                    new_color_row.append((random.choice(dominant_colors), 0)) # born, new color through random selection in dominant color list
                else:
                    new_row.append(0) # even though no changes were made, future generation needs to know that

                    # The same structure for calculating color fading used above -  should make this a function aaahh
                    faded_color_list = []

                    for c in color:

                        faded_value = int(c * (fade_decay_rate * fade_count))

                        min_allowed_value = int(c * min_brightness_factor)
                        final_value = max(faded_value, min_allowed_value)
                        faded_color_list.append(final_value)

                    faded_color = tuple(faded_color_list)
                    new_color_row.append((faded_color, fade_count))

        new_updated_grid.append(new_row) # Update the grid with the new row
        new_color_grid.append(new_color_row) # Update next generation of grid, with each cell's respective colors

    return new_updated_grid, new_color_grid
