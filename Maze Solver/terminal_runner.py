import msvcrt
from mazegenerator import GENERATE_MAZE
from mazesolver import SOLVE_MAZE

def generate_maze():

    correct_input = False
    while not correct_input:
        try:
            correct_input = True
            size:int = int(input("Please specify the maze size: "))
        except ValueError:
            correct_input = False
        try:
            if size < 5:
                correct_input = False
                print("The dimensions you provided are too small. Please try again.")
        except UnboundLocalError:
            correct_input = False
        
        if correct_input == False:
            print("Invalid input, try again.")
        
    GENERATE_MAZE("Maze Solver/maze.txt", True, size)

def solve_maze():
    SOLVE_MAZE("Maze Solver/maze.txt")

while True:
    print("Would you like to [g]enerate a maze, [s]olve a maze, do [b]oth, or [q]uit?")
    user_input = str(msvcrt.getche())[2].lower()
    print("\n")
    
    from mazesolver import SOLVE_MAZE
    if user_input == "g":
        generate_maze()
    
    elif user_input == "s":
        solve_maze()
    
    elif user_input == "b":
        generate_maze()
        solve_maze()
    
    elif user_input == "q":
        break
    
    else:
        print("Invalid input, try again.")