import math
import sys
import msvcrt
from tictactoe_lib import TicTacToe, minimax, N


def make_ai_move():
    move = minimax(game)
    return game.resulting_game(move)

def make_custom_move(user_input:int):
    numpad_location = user_input - 1
    move = (2 - math.floor(numpad_location / 3), numpad_location % 3)
    if game.board[move[0]][move[1]] == N:
        return game.resulting_game(move)
    else:
        print("You cannot move there")
        return game

if __name__ == "__main__":
    game = TicTacToe()
    while True:
        game_over = game.terminal()

        if game_over:
            print(str(game) + "\n" + (game.winner() if game.winner() != N else "Nobody"), "has won. You can [r]estart, or [q]uit")
        else:
            print(str(game) + "\n" + "1-9 to play, 0 for AI move, [r]estart, or [q]uit")
        
        user_input = str(msvcrt.getch())[2].lower()

        if not game_over and user_input.isdigit():
            if int(user_input) == 0:
                print("AI thinking...")
                game = make_ai_move()
            else:
                game = make_custom_move(int(user_input))
        elif user_input == "r":
            game = TicTacToe()
        elif user_input == "q":
            sys.exit()
        else:
            print("Invalid input, try again")
            continue