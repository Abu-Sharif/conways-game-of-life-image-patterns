from collections import Counter

# Removes any background colors, black, greys, whites that we don't want to be used to represent cells
def remove_background_colors(color):

    r, g, b = color

    # If the color is very dark or very light, it is likely a background color, which we don't want
    brightness = r + g + b / 3 # if low likely a dark background
    if brightness > 240 or brightness < 15:
        return True # Likely a background color

    # Checks to see if the colors are grayish by checking if max difference between the values is minimal
    # Usually when the difference between these numbers is low, it results in gray values which we don't want
    max_difference = max(abs(r-g), abs(g-b), abs(b-r)) # abs() used to avoid negative values
    if max_difference < 15:
        return  True # Likely a background color

    return False # Likely not a background color


# Returns a selection of dominant colors found in the original image, returns the highest occuring ones
def get_dominant_color(pixels, amount_of_dominant_colors):
    color_counter = Counter() # Count the amount of occurances of the certain colors, to find dominant ones

    for row in pixels:
        for color in row:
            if remove_background_colors(color): # If background color, skip to next color in row
                continue

            # else if it's not a background color
            # Since we cannot store every color occurance, we group it into similar color buckets by uses 32 multiple
            normalized_color = (
                (color[0] // 32) * 32, #rgb value of red being averaged
                (color[1] // 32) * 32, #green being averaged
                (color[2] // 32) * 32, #blue being averaged
            )
            color_counter[normalized_color] += 1

    # Each color that appears in the image, along with it's # of occurances
    most_common_colors_with_counter = color_counter.most_common(amount_of_dominant_colors)
    most_common_colors = []

    # going through each color and count pair and adding it to the list of most common colors
    for color, count in most_common_colors_with_counter:
        most_common_colors.append(color)
    return(most_common_colors)