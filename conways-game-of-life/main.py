import time

from BMPImage import initialize_grid_from_the_image, read_bmp
from PyGameSetup import display_image_grid

def main():
    interval_time = 300
    image_file = 'assets/morrocan_tile.bmp'
    # Grab the individual pixel values from a image that we select
    image_pixels, image_height, image_width = read_bmp(image_file)


    binary_grid_representation, color_representations, dominant_colors = initialize_grid_from_the_image(image_pixels)

    # Display the grid representation on PyGame, with the generation interval time
    display_image_grid(binary_grid_representation, color_representations, dominant_colors, interval_time)

if __name__ == "__main__":
    main()