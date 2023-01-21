"""
CS5001, Fall 2022
Parth Malik
Final Project - Driver File 

This program is a driver file for our puzzle game
"""

from Turtleplay import TurtlePlay

def main():
    """
    Function -- main 
    This function calls methods from our TurtlePlay class and executs our game 
    
    Parameters:
              None
    
    Returns: 
            None
    """

    tp = TurtlePlay()
    tp.splash_screen()
    tp.dialogue_boxes()
    tp.frame()
    tp.register_images()
    tp.board = tp.create_tiles()
    tp.draw_board()
    tp.scramble_board()
    tp.screen.mainloop() 
    
    
if __name__ == '__main__':
    main()