from enum import Enum
from colorama import Fore
import mazelib as m
import string
import math

class Action(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)

def perform_action(action:Action, parent_node:m.Node) -> m.ChildNode:
    new_coords = (tuple(sum(x) for x in zip(parent_node.coordinates, action.value)))
    return m.ChildNode(new_coords, parent_node)

def int_to_alphadecimal(input:int) -> str:
    return string.ascii_letters[math.floor(input / 10) % len(string.ascii_letters)] + str(input)[-1]

def solve(maze:m.MazeObject):
    frontier_nodes:m.A_Star = m.A_Star()
    frontier_nodes.add_node(m.Node(maze.start_node))
    explored_coords:list[tuple[int,int]] = []

    winning_node = None
    
    while True:
        if frontier_nodes.get_length() == 0:
            break

        current_node = frontier_nodes.get_node()

        if current_node.coordinates not in explored_coords:
            explored_coords.append(current_node.coordinates)
        
        if maze.end_node == current_node.coordinates:
            winning_node = current_node
            break

        for action in Action:
            new_node = perform_action(action, current_node)
            if ((new_node.coordinates not in explored_coords) and
                maze.get_value_at_coords(new_node.coordinates) != m.wall[0]):
                new_node.value = (abs(new_node.coordinates[0] - maze.end_node[0])
                               +  abs(new_node.coordinates[1] - maze.end_node[1]))
                frontier_nodes.add_node(new_node)
    return (winning_node, explored_coords)
    
    

# THE TEST
def SOLVE_MAZE(maze_file_path:str):
    maze = m.MazeObject.from_file(maze_file_path)

    (winning_node, explored_coords) = solve(maze)

    if winning_node != None:
        overrides:list[tuple[tuple[int, int], str, str]] = []
        winning_path_nodes:list[m.Node] = winning_node.find_lineage()
        
        if m.show_path and m.show_explored:
            for i in range(len(explored_coords)):
                if explored_coords[i] in [node.coordinates for node in winning_path_nodes]:
                    overrides.append((explored_coords[i], int_to_alphadecimal(i), Fore.GREEN))
                else:
                    overrides.append((explored_coords[i], int_to_alphadecimal(i), Fore.LIGHTRED_EX))
        elif m.show_path:
            for winning_path_node in winning_path_nodes:
                overrides.append((winning_path_node.coordinates, int_to_alphadecimal(winning_path_node.path_cost), Fore.GREEN))
        elif m.show_explored:
            for i in range(len(explored_coords)):
                overrides.append((explored_coords[i], int_to_alphadecimal(i), Fore.LIGHTRED_EX))
        
        print(maze.render_maze_pretty(overrides))

        if m.show_node_stats:
            print("Nodes explored = " + str(len(explored_coords)))
            print("Nodes to finish = " + str(winning_node.path_cost))

    else:
        overrides:list[tuple[tuple[int, int], str, str]] = []
        if m.show_explored:
            for i in range(len(explored_coords)):
                overrides.append((explored_coords[i], int_to_alphadecimal(i), Fore.LIGHTRED_EX))
        
        print(maze.render_maze_pretty(overrides))
        print("! No path found !")
        
        if m.show_node_stats:
            print("Nodes explored = " + str(len(explored_coords)))