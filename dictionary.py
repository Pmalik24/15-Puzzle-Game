import os
def create_dictionary():

    """
    Function -- create_dictionary
    This funcition first iterates over the files in our root directory
    reads files that end with - '.puz' and validates the files 
    based on the valid numbers (16, 9 or 4) for our puzzle game. 
    Then it reads data from the validated files and creates several dictionaries 
    and a list, which are used later in out TurtlePlay class

    Parameters:
    None

    Returns: main_dict (dictionary):
                key --  puzzle names
                value -- list of image paths in the solved configuration
             tile_size_dict (dictionary):
                key --  puzzle names
                value -- integers representing tile sizes
             thumbnail_dict (dictionary):
                key --  puzzle names
                value -- list of image paths for the thumbnail pics 
             grid_tile_size_dict (dictionary):
                key --  puzzle names
                value -- list of integers representing the number of rows/columns in a square grid
             valid_files (list) -- list of valid files 
    
    """

    file_path = f'./'
    main_dict = {}
    thumbnail_dict = {}
    tile_size_dict = {}
    grid_tile_size_dict = {}
    valid_files = []


    for folders in os.listdir(file_path):
        if folders.endswith('.puz'):
            with open(f'{file_path}/{folders}', 'r') as files:
                lines = files.readlines()
                grid_size = lines[1:2]

                for y in range(len(grid_size)):
                    grid_size[y] = grid_size[y].strip('\n')
                    grid_size[y] = grid_size[y].lstrip('number: ')
                grid_size = ''.join(grid_size)
                grid_size = int(grid_size)
                
                if grid_size == 16 or grid_size == 9 or grid_size == 4:
                    valid_files.append(folders)

        if folders in valid_files:
            with open(f'{file_path}/{folders}', 'r') as files:
                lines = files.readlines()
                unscrambled = lines[4:]
                thumbnails = lines[3:4]
                grid_size = lines[1:2]
                id = lines[4:]
                size = lines[2:3]
                

                for x in range(len(unscrambled)):
                    unscrambled[x] = unscrambled[x][2:]
                    unscrambled[x] = unscrambled[x].lstrip(': ')
                    unscrambled[x] = unscrambled[x].strip('\n')


                for items in range(len(thumbnails)):
                    thumbnails[items] = thumbnails[items].lstrip('thumbnail: ')
                    thumbnails[items] = thumbnails[items].strip('\n')
                thumbnails = ''.join(thumbnails)
    
                for each in range(len(size)):
                    size[each] = size[each].strip('\n')
                    size[each] = size[each].lstrip('size: ')
                size = ''.join(size)
                size = int(size)

                for y in range(len(grid_size)):
                    grid_size[y] = grid_size[y].strip('\n')
                    grid_size[y] = grid_size[y].lstrip('number: ')
                grid_size = ''.join(grid_size)
                grid_size = int(grid_size)
                if grid_size == 16:
                    grid_size = 4
                elif grid_size == 9:
                    grid_size = 3
                elif grid_size == 4:
                    grid_size = 2
            main_dict[folders.strip('.puz')] = unscrambled
            thumbnail_dict[folders.strip('.puz')] = thumbnails
            tile_size_dict[folders.strip('.puz')] = size
            grid_tile_size_dict[folders.strip('.puz')] = grid_size

    return main_dict, tile_size_dict, thumbnail_dict, grid_tile_size_dict, valid_files