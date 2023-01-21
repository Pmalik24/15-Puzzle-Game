'''
CS5001, Fall 2022
Parth Malik
Final Project - Class TurtlePlay

This program contains a class for the tile game

Note:
    My image_placement & error_message methods both work fine,
    but for some reason when I call my image_placement method 
    to display win/loose messages turtle shows the images 
    when I dont quit the program. If quit() is uncommented 
    the images are not shown, time.sleep() and quit() 
    functions are executed and the program quits. 

    I request the grader to comment/uncomment line 322 and/or 330
    to check the functionality 

    I consulted 2 TA's and both of them told me that it's a turtle issue
    and I should not worry about it 
'''

from turtle import Turtle, Screen, bye
from dictionary import create_dictionary
from datetime import datetime
import random
import time

class TurtlePlay:
    """
    Class -- Turtle Play
    Attributes: None
    Methods: 
        board
        click_button
        create_tiles
        dialogue_boxes
        distance
        draw_board
        draw_circle_button
        draw_rect_button
        draw_rectangle
        error_messages
        find_empty_square_pos
        frame
        image_placement
        is_adjacent
        item_index
        leaderboard
        log
        new_puzzle
        register_images
        reset_board
        scramble_board
        splash_screen
        swap_tile
        text_at_xy
        turtle_text_xy
        win    
    """

    def __init__(self):
        """
        Constructor -- __init__ 
        Create a new TurtlePlay instance in which 
        the default game board (4X4) is set for the mario puzzle 
       
        Parameters:
        self - the current instance
       
        Returns: 
                None
        """

        self.screen = Screen()
        self.screen.setup(width=1000, height=1000)
        self.screen.bgpic('./Resources/splash_screen_big.gif')
        self.screen.listen()
        self.turtle = Turtle(visible=False)
        self.turtle.speed(0)
        self.screen.onscreenclick(self.click_button)
        self.moves_played = 0

        # all dictionaries have data from only validated files 
        self.img_dict = create_dictionary()[0] # gif 16-blank
        self.tile_size_dict = create_dictionary()[1] # ints of pixel size
        self.thumbnail_dict = create_dictionary()[2] # strings of thumbnail paths
        self.gridsize_dict = create_dictionary()[3]  # 4x4, 3x3, 2x2 etc
        self.valid_files = create_dictionary()[4] # only validated files 

        # empty lists for later use in the program
        self.tile_list = []
        self.leaders = []
        self.player_name = ''
        
        self.scramble_intensity = 100
        self.root_path = './'

        self.working_lst = self.img_dict['mario']
        self.num_columns = self.gridsize_dict['mario']
        self.num_rows = self.gridsize_dict['mario']
        self.tile_height = self.tile_size_dict['mario']
        self.tile_width = self.tile_size_dict['mario']
        self.board = self.board()
        self.puzzle_choice = 'mario.puz'

        self.txt_turtle = Turtle(visible=False)

        # creating a flag to indicate if the game is currently being played
        self.is_playing = False

        # error flags
        self.file_error = False
        self.leaderboard_error = False

    def new_puzzle(self, chosen):
        """
        Method -- new_puzzle 
        This method clears the screen, redraws the frame, 
        resets the gameboard's dimension based on which puzzle the user chooses
        and redraws the game board, giving the user a fresh puzzle to play
        
        Parameters:
        self -- the current instance
        chosen -- the users puzzle choice 
    
        Returns: 
                None
        """

        chosen = self.puzzle_choice
        chosen = chosen.strip('.puz')
        
        self.working_lst = self.img_dict[chosen]
        self.num_columns = self.gridsize_dict[chosen]
        self.num_rows = self.gridsize_dict[chosen]
        self.tile_height = self.tile_size_dict[chosen]
        self.tile_width = self.tile_size_dict[chosen]
        
        self.board = [["#" for _ in range(self.num_columns)] for _ in range(self.num_rows)]
    
        self.moves_played = 0
        self.screen.clear()
        self.screen.tracer(0)
        self.screen.onscreenclick(self.click_button)
        self.frame()
        self.image_placement(405,415,f'./button gifs/BLANK.gif')

        self.board = self.create_tiles()
        self.draw_board()
        self.scramble_board()
            
    def board(self):
        """
        Method -- board
        This method creates the solved board (representing a [n X n] GRID) 
        which is used in the constructor to set the default puzzle 

        Parameters:
        self -- the current instance
    
        Returns: 
                board - the board that's been created 
        """

        board = [["#" for _ in range(self.num_columns)] for _ in range(self.num_rows)]
        return board
    
    def log(self):
        """
        Method -- log
        This method writes to the 5001_puzzle.err.txt file
        whenever self.file_error and self.leaderboard_error flags's 
        value changes to true

        Parameters:
        self -- the current instance
    
        Returns: 
                None
        """
            
        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        str_date_time = date_time.strftime("%d %B %Y, %H:%M:%S")

        with open('5001_puzzle.err.txt', 'a+') as file:
            if self.file_error is True:
                file.write(f'{str_date_time}: ERROR: File - {self.puzzle_choice} does not exists LOCATION: Turtleplay.click_button()\n')
            elif self.leaderboard_error is True: 
                file.write(f'{str_date_time}: ERROR: Could not open leaderboard file - Leaderboard Dummy.txt LOCATION: Turtleplay.frame()\n')

    def reset_board(self):
        """
        Method -- reset_board
        This method resets a scrambled board by recreating the tiles and redrawing a solved board

        Parameters:
        self -- the current instance
    
        Returns: 
               None
        """

        # when we load a new game, the player is not playing until the board is completed
        self.is_playing = False
        self.screen.tracer(0)
        self.board = self.create_tiles()
        self.draw_board()
        self.is_playing = True

        self.moves_played = 0
        if self.is_playing:
            self.text_at_xy(-410,-400, f'Player Moves: {self.moves_played}', 'black')

    def item_index(self,lst, item):
        """
        Method -- item_index 
        This method iterates over a list and returns the position of an element

        Parameters:
        self -- the current instance
        lst -- the list we want to iterate over 
        item -- the item we want to see the position of 
    
        Returns: 
            The position of the chosen element
        """
        
        for i, j in enumerate(lst):
            if item in j:
                return (i, j.index(item))
                
    def find_empty_square_pos(self):
        """
        Method -- find_empty_square_pos
        This method iterates over our board and finds the empty square
        and returns its position by calling the item_index method

        Parameters:
        self -- the current instance
    
        Returns: 
            The position of the empty square.

        """
        self.screen.tracer(0)
        self.puzzle_choice = self.puzzle_choice.strip('.puz')
        for row in self.board:
            for items in row:
                if items.shape() == f"./Images/{self.puzzle_choice}/blank.gif":
                    empty_square = items

        return self.item_index(self.board, empty_square)
    
    def is_adjacent(self,el1, el2):
        """
        Method -- is_adjacent
        This method check whether two elements in a 2D list are adjacent
        by calling the builtin abs (absolute value) function

        Parameters:
        self -- the current instance
        el1 -- the first element 
        el2 -- the second element 
    
        Returns: 
            True is the elements are adjacent, else false 

        """

        if abs(el2[1] - el1[1]) == 1 and\
           abs(el2[0] - el1[0]) == 0:
            return True
        if abs(el2[0] - el1[0]) == 1 and\
           abs(el2[1] - el1[1]) == 0:
            return True
        return False
    
    def win(self):
        """
        Method -- win
        This method checks if the player has won or lost  the game based on 
        the player's chosen number of moves and the player's number of moves played.

        Parameters:
        self -- the current instance
    
        Returns: 
            None
        """

        i = 0
        flag = True
        for each in range(len(self.board)):
            for tile in range(len(self.board[each])):
                if str(self.board[each][tile]) != str(self.tile_list[i]):
                    flag = False
                i += 1
        
        if flag is True and self.moves_played < self.moves_chosen:
            try:
                with open('Leaderboard Dummy.txt', 'r+') as file:
                    lines =  file.readlines()
                    for items in lines:
                        items = items.split()
                        moves = int(items[0])
                        name = items[1]
                        name_move = [moves, name]                        
                        self.leaders.append(name_move)
                    self.leaders.append([self.moves_played, self.player_name])
                    self.leaders = sorted(self.leaders, key=lambda x:x[0])
                    file.write(f'\n{self.moves_played} {self.player_name}')
                        
            except FileNotFoundError:
                with open('Leaderboard Dummy.txt', 'a') as file:
                    file.write(f'{self.moves_played} {self.player_name}')
                    self.turtle_text_xy(211,323,f'{self.moves_played}: {self.player_name}', 'green')

            self.image_placement(0,0,'./Resources/winner.gif')
            time.sleep(3)
            quit()  
            # Please refer to the note on the top of this file in line 8

        elif flag is False and self.moves_played >= self.moves_chosen:
            self.image_placement(0,-300,'./Resources/Lose.gif')
            time.sleep(3)
            self.image_placement(0,-300,'./Resources/credits.gif')
            time.sleep(3)
            quit()
            # Please refer to the note on the top of this file in line 8

    def leaderboard(self):
        """
        Method -- Leaderboard
        This method reads form the Leaderboard Dummy.txt file, creates a nested list of 
        with player moves as the first element element and player name as the second element of the 
        sublists, sorts the nested list on player moves and writes that data to the leaderboard 
        section of our frame

        Parameters:
        self -- the current instance

        Returns: 
            None
        """
        with open('Leaderboard Dummy.txt', 'r') as file:
            lines = file.readlines()
            for x in range(len(lines)):
                lines[x] = lines[x].strip('\n')
                lines[x] = lines[x].split()
            lines = sorted(lines, key=lambda x:int(x[0]))

        y_cord = 323
        for i in lines:
            self.turtle_text_xy(211,y_cord,f'\n{i[0]} - {i[1]}\n', 'green')
            y_cord -= 25 

    def draw_board(self):
        """
        Method -- draw_board
        This method draws the gameboard i.e. (our nested list of turtle objects) on the screen

        Parameters:
        self -- the current instance

        Returns: 
            None
        """

        self.screen.tracer(0)
        self.puzzle_choice = self.puzzle_choice.strip('.puz')

        for i in range(self.num_rows):
            for j in range(self.num_columns):
                tile = self.board[i][j]
                tile.showturtle()
                home_x = -300 + j * (self.tile_width + 2)
                home_y = 300 - i * (self.tile_height + 2)
                tile.goto(home_x, home_y)

        self.image_placement(405,415,f'./Images/{self.puzzle_choice}/{self.puzzle_choice}_thumbnail.gif')
        self.screen.tracer(1)
    
    def swap_tile(self, tile):
        """
        Method -- swap_tile
        This method swaps the position of the clicked tile with the empty tile 
        inside the current board list and redraws the board after each successful swap
        
        Parameters:
        self -- the current instance
        tile -- the tile that we will swap with the empty tile

        Returns: 
            None
        """

        current_i, current_j = self.item_index(self.board, tile)
        empty_i, empty_j = self.find_empty_square_pos()
        empty_square = self.board[empty_i][empty_j]
        swap = False

        if self.is_adjacent([current_i, current_j], [empty_i, empty_j]):
            temp = self.board[empty_i][empty_j]
            self.board[empty_i][empty_j] = tile
            self.board[current_i][current_j] = temp
            swap = True
            self.draw_board() 

        # using the is_playing flag to indicate when to update
        if self.is_playing and swap is True:
            self.moves_played +=1 
            self.text_at_xy(-410,-400, f'Player Moves: {self.moves_played}', 'black')
            self.win()
   
    def create_tiles(self):
        """
        Method -- create_tiles(self)
        Creates and returns a list (our board) of tiles based on turtle objects
        in the winning configuration

        Parameters:
        self -- the current instance

        Returns: 
            self.board - the current solved board 
        """

        self.screen.tracer(0)
        id = 0
        self.tile_list.clear()
        for i in range(self.num_rows): #3
            for j in range(self.num_columns): #3
                tile_num = (self.num_columns * i + j) #0
                tile = Turtle(f'./{self.working_lst[tile_num]}', id)
                self.tile_list.append(tile)
                tile.penup()
                self.board[i][j] = tile

                def click_callback(x, y, tile=tile):
                    self.screen.tracer(0)
                    """Passes `tile` to `swap_tile()` function."""
                    return self.swap_tile(tile)

                tile.onclick(click_callback)  
                id += 1

        return self.board

    def text_at_xy(self, x, y, text, color):
        """
        Method -- text_at_xy
        This method make the current turtle go to a specific position and writes some text

        Parameters:
        self -- the current instance
        x -- the x coordinate we want our turtle to go to
        y --  the y coordinate we want our turtle to go to
        text --  the text we want to display 
        color --  text colour we want (default color is black)

        Returns: 
            self.board - the current solved board 
        """

        self.screen.tracer(0)
        self.txt_turtle.clear()
        self.txt_turtle.color(color)
        self.txt_turtle.penup()
        self.txt_turtle.goto(x, y)
        self.txt_turtle.write(text, font=("Arial", 32, "bold"))

    def turtle_text_xy(self, x, y, text, color='black'): 
        """
        Method -- turtle_text_xy:
        This method creates a new turtle, which goes to a specific position and writes some text

        Parameters:
        self -- the current instance
        x -- the x coordinate we want our turtle to go to
        y --  the y coordinate we want our turtle to go to
        text --  the text we want to display 
        color --  text colour we want (default color is black)

        Returns: 
            self.board - the current solved board 
        """

        t = Turtle()
        second_t = Turtle()
        t.hideturtle()
        self.screen.tracer(0)
        t.clear()
        t.color(color)
        t.penup()
        t.goto(x, y)
        t.write(text, font=("Arial", 30, "bold"))

    def error_messages(self, image_path):
        """
        Method -- error_messages
        This method shows images at (x,y = 0,0) coordinate, delays execution by 3 second
        and then hides the turtle so that the image is no longer visible

        Parameters:
        self -- the current instance
        image_path -- the path of the image

        Returns: 
            None
        """

        t = Turtle(visible=False)
        t.speed(0)
        self.screen.register_shape(image_path)
        t = Turtle(shape=image_path)
        time.sleep(3)
        t.hideturtle()

    def dialogue_boxes(self):  
        """
        Method -- dialogue_boxes
        This method calls Turtle's inbuilt functions for capturing some numeric and 
        alphabetical input from the user and stores them in separate variables

        Parameters:
        self -- the current instance

        Returns: 
            None
        """
          
        self.player_name = self.screen.textinput('Ask Name', 'Please Enter Yout Name:')
        num_str = 'Enter the number of moves (chances) you want (5 - 200)'
        self.moves_chosen = self.screen.numinput('Move Count', num_str, 0, minval= 5, maxval= 200)
        

    def draw_rect_button(self, x, y, length, width):
        """
        Method -- draw_rect_button
        This method makes the turtle go to a specific position and draw a color filled rectangle, 
        which acts as a frame for our button as we will place an image over that rectangle

        Parameters:
            self -- the current instance
            x -- x coordinate at which we want to start drawing the frame 
            y -- y coordinate at which we want to start drawing the frame 
            length -- length of the button
            width -- width of the button

        Returns: 
                None
        """

        self.screen.tracer(0)
        self.turtle.penup()
        self.turtle.begin_fill()
        self.turtle.goto(x, y)
        self.turtle.goto(x + length, y)
        self.turtle.goto(x + length, y - width)
        self.turtle.goto(x, y - width)
        self.turtle.goto(x, y)
        self.turtle.end_fill()

    def draw_circle_button(self, x, y, radius):
        """
        Method -- draw circle_button
        This method makes the turtle go to a specific position and draw a color filled circle
        which acts as a frame for our button as we will place an image over that circle.

        Parameters:
            self -- the current instance
            x -- x coordinate at which we want to start drawing the frame 
            y -- y coordinate at which we want to start drawing the frame 
            rdaius the radius of our circlular frame  

        Returns: 
                None
        """

        self.turtle.pencolor('white')
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.begin_fill()
        self.turtle.circle(radius)
        self.turtle.end_fill()
        self.turtle.pencolor('black')
        self.turtle.goto(x,y)

    def draw_rectangle(self, x, y, length, width, color='black'):
        """
        Method -- draw rectangle
        This method makes the turtle draw a border in the shape of a rectangle.

        Parameters:
            self -- the current instance
            x -- x coordinate at which we want to start drawing  
            y -- y coordinate at which we want to start drawing 
            length -- length of the rectangle 
            width --  length of the rectangle 
            color(optional) -- color of turtle pen (default is black)
            rdaius the radius of our circlular frame  

        Returns: 
                None
        """
        self.turtle = Turtle(visible=False)
        self.turtle.speed(0)
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.pendown()
        self.turtle.width(8)
        self.turtle.forward(width)
        self.turtle.right(90)
        self.turtle.forward(length)
        self.turtle.right(90)
        self.turtle.forward(width)
        self.turtle.right(90)
        self.turtle.forward(length)
        self.turtle.right(90)

    def distance(self, point_1, point_2):
        """
        Method -- distance 
        This method calculates the distance between two points in a cartesian plane

        Parameters:
            self -- the currebt instance 
            point_1 - the first point
            point_1 - the second point

        Returns: 
                distance -- the distance between the two points
        """

        distance = (point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2 
        return distance
    
    def splash_screen(self):
        """
        Method -- splash screen 
        This method suspends the code execution for three seconds
        and then removes the background from the screen

        Parameters:
            self -- the current instance 

        Returns: 
                None
        """

        time.sleep(3)
        self.screen.bgpic('nopic')
        
    def image_placement(self, x, y, image_path):
        """
        Method -- image_placement
        This method places images on certain x,y coordinates
        using Turtle's builtin stamp mthod

        Parameters:
            self -- the currebt instance 
            x -- the x coordinate where we want to place an image over
            y -- the y coordinate where we want to place an image over
            image_path -- the path of the image we want to use 

        Returns: 
                None
        """

        t = Turtle(visible=False)
        t.speed(0)
        self.screen.register_shape(image_path)
        t = Turtle(shape=image_path)
        t.penup()
        t.goto(x,y)
        t.stamp()


    def click_button(self,x, y):
        """
        Method -- click_button
        This method uses conditionals to detect weather the user clicks on a button or not
        if the click is on or inside the perimeter of our buttons
        quit  --> program displays a quit message, credits and then quits
        load  -->  program prompts the user to choose a new puzzle and then loads it 
                 using the new_puzzle method
        reset --> program resets the board to a solved board using the reset_board method

        Parameters:
            self -- the currebt instance 
            x -- the x coordinate of the click
            y -- the y coordinate of the click

        Returns: 
                None
        """

        # load
        if x <= 256\
        and x >= 115\
        and y <= -309\
        and y >= -444:

            self.is_playing = False
            self.moves_played = 0
            choices =  '\n'.join(self.valid_files)
            choices = '\n' + choices
            string = f'Enter the name of the puzzle you want to choose{choices}'
            self.puzzle_choice = self.screen.textinput('Choice of Puzzle', string)

            if self.puzzle_choice not in self.valid_files:
                self.error_messages('./Resources/file_error.gif')
                self.file_error = True
                self.log()

            elif self.puzzle_choice == None:
                pass

            else:
                if len(self.valid_files) > 10:
                    self.error_messages('./Resources/file_warning.gif')
                    self.valid_files = self.valid_files[:11]
                for i in range(len(self.valid_files)):
                        if self.puzzle_choice == self.valid_files[i]:
                            self.new_puzzle(self.puzzle_choice)

        # quit
        elif x <= 420\
        and x >= 280\
        and y <= -322.5\
        and y >= -427.5:

            # Please refer to the note on the top of this file in line 8
            self.image_placement(0, 0, 'Resources/quitmsg.gif')
            time.sleep(3)
            self.image_placement(0, 0, 'Resources/credits.gif')
            time.sleep(3)
            quit()

        # reset
        elif self.distance((25,-375), (x,y)) <= 70 ** 2:
            self.reset_board()

    def frame(self):
        """
        Method -- frame
        This method creates the frame for our game by calling other methods

        Parameters:
            self -- the current instance 
            
        Returns: 
                None
        """

        # drawing leaderboard 
        invalid_str = 'no leaderboard er'
        try: 
            if self.player_name != invalid_str or\
                self.player_name != invalid_str.capitalize() or\
                    self.player_name != invalid_str.upper():
                self.leaderboard()

        except IOError:
            self.error_messages('./Resources/leaderboard_error.gif')
            self.leaderboard_error = True
            self.log()
        
        self.draw_rectangle(-450, 450, 700, 600)

        self.draw_rectangle(200, 450, 700, 250, 'green')
        
        self.draw_rectangle(-450, -300, 150, 900)

        # reset
        self.draw_circle_button(25, -445, 70)
        # load 
        self.draw_rect_button(115, -305, 140, 140)
        # quit
        self.draw_rect_button(280, -322.5, 140, 105)

        # image paths
        reset_image = f'./button gifs/Reset.gif'
        load_image = f'./button gifs/load.gif'
        quit_image = f'./button gifs/Quit.gif'
        self.image_placement(25, -375,reset_image)

        self.image_placement(185, -375,load_image)
        self.image_placement(350, -375,quit_image)

        # txt placement
        txt = self.text_at_xy(-410, -400, f'PLAYER MOVES: {self.moves_played}', 'black') 
        txt_2 = self.turtle_text_xy(206, 415, f'Leaders:', 'green') 



    def register_images(self):
        """
        Method -- frame
        This method creates the frame for our game by calling other methods

        Parameters:
            self -- the current instance 
            
        Returns: 
                None
        """

        for key,values in self.img_dict.items():
            for lsts in values:
                self.screen.addshape(f'./{lsts}')
          
    def scramble_board(self):
        """
        Method -- scramble_board
        This method scrambles our gamee board i.e. the list of turtle objects

        Parameters:
            self -- the current instance 
            
        Returns: 
                None
        """

        self.screen.tracer(0)
        self.puzzle_choice = self.puzzle_choice.strip('.puz')
        for i in range(self.scramble_intensity):
            for row in self.board:
                for items in row:
                    if items.shape() == f'./Images/{self.puzzle_choice}/blank.gif':
                        empty_square = items

            empty_i, empty_j = self.find_empty_square_pos()
            directions = ["up", "down", "left", "right"]

            if empty_i == 0: directions.remove("up")
            if empty_i >= self.num_rows - 1: directions.remove("down") 
            if empty_j == 0: directions.remove("left")
            if empty_j >= self.num_columns - 1: directions.remove("right") 

            direction = random.choice(directions)

            if direction == "up": self.swap_tile(self.board[empty_i - 1][empty_j])
            if direction == "down": self.swap_tile(self.board[empty_i + 1][empty_j])
            if direction == "left": self.swap_tile(self.board[empty_i][empty_j - 1])
            if direction == "right": self.swap_tile(self.board[empty_i][empty_j + 1])
        
        # after the board is shuffled, the player starts playing
        self.is_playing = True