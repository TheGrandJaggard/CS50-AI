# All credit to https://github.com/NathansProgramming/MazeGeneratorRepo/blob/main/MazeGenerators/2dmazegenerator.py
import random
from typing import List
import mazelib as m

def create_base_maze(ln, wd) -> m.MazeObject:
    # Creates maze by making a double nested list with all the characters being walls.
    maze:List[List[int]] = []       # the list that will be holding the maze
    for y in range(0, wd):          # keep making lines of characters for how much width there is.
        line:List[int] = []         # lines hold a line of characters.
        for x in range(0, ln):      # keep making characters for how much length there is.
            line.append(m.wall[0])  # appends a wall to the list
        maze.append(line)           # appends the list to the maze once all of the walls have been appended.
    return m.MazeObject(maze)       # once finished, return the maze.

def create_start(maze:m.MazeObject) -> m.MazeObject:
    starting_y = random.randint(1, maze.get_size()[0] - 2)  # makes a random y-coordinate (height)
    starting_x = random.randint(1, maze.get_size()[1] - 2)  # makes a random x-coordinate (width)
    
    maze.node_array[starting_y][starting_x] = m.start[0]
    maze.update_changes()
    return maze

def create_maze_body(maze:m.MazeObject) -> m.MazeObject:
    # add in the walls that are around the beginning cell to begin the fun.
    starting_y = maze.start_node[0]
    starting_x = maze.start_node[1]
    walls = [[starting_y - 1, starting_x], [starting_y, starting_x - 1],
                [starting_y, starting_x + 1], [starting_y + 1, starting_x]]
    
    while len(walls) > 0:  # while there are still walls in the walls list. Yes, it does have to be len(walls).
        rando_choice = random.randint(0, len(walls) - 1)  # gets a random index to choose from
        random_wall = walls[rando_choice]  # uses that random index to get a random wall from the walls list.
        if random_wall[0] < 1 or random_wall[0] > maze.get_size()[0] - 2:  # if the wall is out of bounds, remove and start again.
            del walls[rando_choice]
            continue
        if random_wall[1] < 1 or random_wall[1] > maze.get_size()[1] - 2:
            del walls[rando_choice]
            continue
        if maze.get_value_at_coords((random_wall[0], random_wall[1])) == m.passage[0]:  # if the "wall" is actually a cell, remove and start again.
            del walls[rando_choice]
            continue

        # keeps track of how many cells are nearby the wall. As long as it's less than 2, the wall will become a cell.
        cell_count = 0
        if random_wall[0] - 1 < 0:  # if the random wall's neighbor is out of bounds, don't check if it's a cell.
            cell_count = cell_count  # random code to do something other than nothing or something bad
        elif maze.get_value_at_coords((random_wall[0] - 1, random_wall[1])) == m.passage[0]:  # if the neighbor is a cell, increment cell count.
            cell_count += 1

        if random_wall[0] + 1 > maze.get_size()[0] - 1:
            cell_count = cell_count
        elif maze.get_value_at_coords((random_wall[0] + 1, random_wall[1])) == m.passage[0]:
            cell_count += 1

        if random_wall[1] - 1 < 0:
            cell_count = cell_count
        elif maze.get_value_at_coords((random_wall[0], random_wall[1] - 1)) == m.passage[0]:
            cell_count += 1

        if random_wall[1] + 1 > maze.get_size()[0] - 1:
            cell_count = cell_count
        elif maze.get_value_at_coords((random_wall[0], random_wall[1] + 1)) == m.passage[0]:
            cell_count += 1

        if cell_count < 2:  # if the wall passed the cell check, make it a cell and try to add the neighboring walls.
            maze.node_array[random_wall[0]][random_wall[1]] = m.passage[0]
            try:
                walls.append([random_wall[0] - 1, random_wall[1]])
            except IndexError:
                pass
            try:
                walls.append([random_wall[0] + 1, random_wall[1]])
            except IndexError:
                pass
            try:
                walls.append([random_wall[0], random_wall[1] - 1])
            except IndexError:
                pass
            try:
                walls.append([random_wall[0], random_wall[1] + 1])
            except IndexError:
                pass
            del walls[rando_choice]  # once done with adding neighboring walls, delete itself in the walls list
        else:  # if the wall had 2 or more cells nearby, delete itself in the walls list and go back to the start
            del walls[rando_choice]
    # make sure there is a start cell
    if maze.start_node == (-1, -1):
            maze.node_array[starting_y][starting_y] = m.start[0]
    maze.update_changes()
    return maze

def create_standard_start_and_finish(maze:m.MazeObject) -> m.MazeObject:
    maze.node_array[maze.start_node[0]][maze.start_node[1]] = m.passage[0]
    starting_y = 1
    starting_x = 1
    maze.node_array[starting_y][starting_x] = m.start[0]
    while True:
        starting_y += 1
        if maze.get_value_at_coords((starting_y, starting_x)) == m.wall[0]:
            maze.node_array[starting_y][starting_x] = m.passage[0]
        else:
            break

    ending_y = maze.get_size()[0] - 2
    ending_x = maze.get_size()[1] - 2
    maze.node_array[ending_y][ending_x] = m.end[0]
    while True:
        ending_y -= 1
        if maze.get_value_at_coords((ending_y, ending_x)) == m.wall[0]:
            maze.node_array[ending_y][ending_x] = m.passage[0]
        else:
            break
    maze.update_changes()
    return maze

def create_random_finish(maze:m.MazeObject) -> m.MazeObject:
    ending_y = random.randint(1, maze.get_size()[0] - 2)
    ending_x = random.randint(1, maze.get_size()[1] - 2)
            
    if ending_y < maze.get_size()[0]/2: go_down = True # if we are above the center of the maze we move downward when looking for a valid place
    else: go_down = False
    while True:
        if maze.get_value_at_coords((ending_y, ending_x)) == m.passage[0]:
            maze.node_array[ending_y][ending_x] = m.end[0]
            break
        else:
            ending_y += (-1 if go_down else 1) # move the starting location down and try again
    maze.update_changes()
    return maze

# THE TEST

def GENERATE_MAZE(output_file_path:str, show_output:bool, size:int):
    the_maze = create_base_maze(size, size)     # create the maze based on the width and height specified.
    the_maze = create_start(the_maze)           # make the random start position in the maze.
    the_maze = create_maze_body(the_maze)       # make the passages and corridor
    if m.random_start_and_end: create_random_finish(the_maze)
    else: create_standard_start_and_finish(the_maze)

    if show_output:
        print(the_maze.render_maze_pretty([]))

    with open(output_file_path, "w") as file:
        file.write(the_maze.render_maze_for_file())