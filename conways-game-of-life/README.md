# Conway's Game of Life with image-based creation. 

A Python implementation of Conway's Game of Life using pygame, to support for custom image-based patterns.


## Features

- Visual representation using pygame
- Custom image patterns (BMP format)
- Color-based cell evolution
- Adjustable generation timing
- Interactive display with keyboard controls

## Requirements

- Python 3.x
- pygame library

## Installation

1. Clone this repository
2. Install pygame:
   ```bash
   pip install pygame
   ```

## Usage

Run the main program:
```bash
python main.py
```

### Controls
- **ESC** or **Close Window**: Exit the program

## Project Structure

```
conways-game-of-life/
├── main.py              # Main program entry point
├── BMPImage.py          # BMP image processing and grid initialization
├── Color.py             # Color analysis and processing
├── PyGameSetup.py       # Pygame display and game loop
├── assets/              # Image assets
│   ├── morrocan_tile.bmp
│   └── andelus_tile.bmp
└── README.md
```

## How It Works

1. Loads a BMP image from the assets folder
2. Converts the image to a binary grid (alive/dead cells)
3. Analyzes colors to create color representations
4. Runs Conway's Game of Life rules on the grid
5. Displays the evolving pattern in real-time

## Customization

- Change the image file in `main.py` (line 8)
- Adjust generation timing with `interval_time` variable
- Modify display settings in `PyGameSetup.py`

## Author

Abu Sharif 
