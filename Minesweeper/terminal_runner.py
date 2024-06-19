import sys
import msvcrt
from minesweeper_lib import Minesweeper, MinesweeperAI

# Board size
SIZE = "medium"
# how often the screen reprints on auto-complete
LIVE_PRINTING_SPEED = 10

def make_all_safe_moves():
    printing_count = 0 # timer that counts up
    while True:
        if game.game_over: print("Somehow I lost making a safe move"); break
        move = ai.make_safe_move()
        if move == None: break
        count = game.process_move(move)
        if count != None: ai.add_knowledge(move, count)
        if LIVE_PRINTING_SPEED != 0:
            if printing_count == LIVE_PRINTING_SPEED:
                printing_count = 0
                print(render_board(game) + "\n")
            else:
                printing_count += 1

def make_move():
    move = ai.make_safe_move()
    if move == None:
        move = ai.make_probable_move()
    if move == None:
        move = ai.make_random_move()
    if move == None:
        return
    count = game.process_move(move)
    if count != None: ai.add_knowledge(move, count)

def initialize_game(size:str) -> tuple[Minesweeper, MinesweeperAI]:
    game = Minesweeper(size)
    ai = MinesweeperAI(game)
    return (game, ai)

def print_sentences():
    print("Sentances:")
    for sentance in ai.knowledge:
        print("   ", sentance)
    print("flags:", game.flags)
    print("moves made:", game.moves)

def make_custom_move():
    while True:
        user_input = input("Enter coordinates, comma delimited\n> ")
        try:
            (i, j) = tuple(int(coord) for coord in user_input.split(","))
            if i < game.height and j < game.width:
                break
        except:
            print("Invalid input, try again")

    count = game.process_move((i, j))
    ai.add_knowledge((i, j), count)

def render_board(game:Minesweeper) -> str:
    raw_board = game.get_board()
    output = "⬜" * (game.width + 2) + "\n"

    for raw_row in raw_board:
        output += "⬜"
        for raw_cell in raw_row:
            if raw_cell == -1:
                output += "🚩"
            elif raw_cell == -2:
                output += "❌"
            elif raw_cell == -3:
                output += "💣"
            elif raw_cell == -4:
                output += "🟩"
            else:
                if raw_cell == 0: output += "  "
                else: output += " " + str(raw_cell)
        output += "⬜\n"
    output += "⬜" * (game.width + 2)
    return output


if __name__ == "__main__":
    (game, ai) = initialize_game(SIZE)
    while True:
        game.flags = ai.known_mines

        if game.game_over:
            print(render_board(game) + "\nYou have been blown up. You can [r]estart, [p]rint knowlage sentances, or [q]uit.")
        else:
            print(render_board(game) + "\nYou can make [a]ll safe moves, make a [m]ove, make a [c]ustom move, [r]estart, or [q]uit.")
        
        user_input = str(msvcrt.getche())[2].lower()
        print("\n")

        if user_input == "a" and not game.game_over:
            make_all_safe_moves()
        elif user_input == "m" and not game.game_over:
            make_move()
        elif user_input == "r":
            (game, ai) = initialize_game(SIZE)
        elif user_input == "p":
            print_sentences()
        elif user_input == "q":
            sys.exit()
        elif user_input == "c" and not game.game_over:
            make_custom_move()
            continue