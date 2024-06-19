from collections import Counter
import math

X = "X"
O = "O"
N = " "

LOG = False

class TicTacToe():
    def __init__(self, board:tuple[tuple] = ((N, N, N), (N, N, N), (N, N, N))):
        self.board = board

    def __str__(self) -> str:
        output = ""
        for i in range(5):
            output += "\n"
            if i % 2:
                output += "⬜⬜⬜⬜⬜"
            else:
                for j in range(5):
                    if j % 2:
                        output += "⬜"
                    else:
                        output += " " + self.board[math.floor(i/2)][math.floor(j/2)]
        return output

    def current_player(self) -> str:
        board_elements = [x for xs in self.board for x in xs]
        element_count = Counter(board_elements)
        if element_count[X] > element_count[O]:
            if LOG: print("player:", O)
            return O
        else:
            if LOG: print("player:", X)
            return X
        
    def possible_actions(self) -> list[tuple]:
        actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == N:
                    actions.append((i, j))
        if LOG: print("possible actions:", actions)
        return actions

    def resulting_game(self, action:tuple):
        if self.board[action[0]][action[1]] == N:
            output_board = list(list(self.board[i]) for i in range(3))

            output_board[action[0]][action[1]] = self.current_player()

            if LOG: print("resulting board:", output_board)
            return TicTacToe(tuple(tuple(output_board[i]) for i in range(3)))
        else:
            if LOG: print("tried to move in occupied cell")
            raise Exception

    def winner(self) -> str:
        if LOG: print("winner checking board:", self.board)

        for player in [X, O]:
            # check row wins
            for row in self.board:
                row_elements = Counter(row)
                if row_elements[player] == 3:
                    return player
                
            # check column wins
            for col_num in range(3):
                col = list(col[col_num] for col in self.board)
                col_elements = Counter(col)
                if col_elements[player] == 3:
                    return player
            
            # check diagonals
            diagonal_1 = list(self.board[i][i] for i in range(3))
            diagonal_1_elements = Counter(diagonal_1)
            if diagonal_1_elements[player] == 3:
                return player
            
            diagonal_2 = list(self.board[2-i][i] for i in range(3))
            diagonal_2_elements = Counter(diagonal_2)
            if diagonal_2_elements[player] == 3:
                return player
            
        return N

    def terminal(self) -> bool:
        if LOG: print("terminal checking board:", self.board)

        return self.winner() != N or self.possible_actions() == []

    def utility(self) -> int: # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
        if LOG: print("utilitizig board:", self.board)

        w = self.winner()
        if w == X:
            return 1
        elif w == O:
            return -1
        else:
            return 0

    def greater_utility(self) -> int: # Returns 1 if X has or will win the game, -1 if O has or will win, 0 otherwise.
        
        if LOG: print("greater utilitising board:", self.board)
        
        if self.terminal():
            return self.utility()
        else:
            mm = minimax(self)
            r = self.resulting_game(mm)
            u = r.utility()
            return u


def minimax(game:TicTacToe, depth= "") -> tuple:
    current_player = game.current_player()
    current_player_preferred_result = (1 if current_player == X else (-1 if current_player == O else 0))

    if LOG: print(current_player, "minmaxing board:", game.board)

    actions_scored = {}
    for action in game.possible_actions():
        result = game.resulting_game(action)
        actions_scored[action] = result.greater_utility()

        if actions_scored[action] == current_player_preferred_result:
            return action
    
    if LOG: print("moves:", actions_scored)

    if current_player == X:
        return max(actions_scored, key=actions_scored.get)
    else:
        return min(actions_scored, key=actions_scored.get)