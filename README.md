# Sliding Puzzle Game

This Sliding Puzzle Game is an interactive and visually appealing Python-based game using Turtle Graphics, designed to provide a fun and engaging experience for users of all ages. The game offers customizable puzzle sizes (2x2, 3x3, and 4x4 grids) and a dynamic interface, catering to various skill levels.

## Features

- Customizable puzzle sizes: Choose between 2x2, 3x3, and 4x4 grids
- Intuitive controls and engaging user experience
- Custom puzzle configuration: Create your own puzzles with unique images and tile sizes
- Leaderboard functionality: Track player performance and moves
- Dynamic interface with appealing visuals
- Error handling: Detect and display error messages for invalid puzzle files or leaderboard issues
- Reset, Load, and Quit buttons for seamless gameplay

## Getting Started

1. Clone the repository to your local machine
2. Ensure Python 3.x is installed on your system
3. Install Turtle Graphics library if not already installed
4. Navigate to the project directory and run `Game_driver.py` to launch the game

## How to Play

1. Upon launching the game, you will be prompted to enter your name
2. Choose a puzzle size (2x2, 3x3, or 4x4) and select a puzzle from the list of valid files
3. Use the left mouse button to click on a tile adjacent to the empty tile to slide it into the empty space
4. Continue sliding tiles until the puzzle is solved, and your moves will be tracked in the leaderboard
5. Use the Reset, Load, and Quit buttons to reset the board, load a new puzzle, or quit the game

## Customizing Puzzles

To create your own custom puzzles, follow these steps:

1. Create a new `.puz` file in the project directory
2. Add the necessary information to the file following this format:

title: Your Puzzle Name
number: Number of tiles (4, 9, or 16)
size: Tile size in pixels
thumbnail: Path to thumbnail image
1: Path to first tile image
2: Path to second tile image
...
n: Path to nth tile image

3. Save the file and load it in the game by selecting it from the list of valid files

## Contributing

Feel free to fork the project, create a feature branch, and submit a pull request to contribute to the project.
