import random

SPECS:dict[str, tuple] = {
    # "size": (height, width, mines)
    "small": (8, 8, 10),
    "medium": (16, 16, 30),
    "large": (16, 30, 99)
}

LOG = False

class Minesweeper():
    def __init__(self, size:str):

        # Set initial stats
        self.height = SPECS[size.lower()][0]
        self.width = SPECS[size.lower()][1]
        self.game_over = False
        self.moves = set()
        self.flags = set()
        self.death_square = None

        # Add mines randomly
        self.mines = set()
        while len(self.mines) != SPECS[size][2]:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) not in self.mines:
                self.mines.add((i, j))
    
    def get_board(self) -> list[list[int]]:
        output = list()
        for row in range(self.height):
            output_row = list()
            for col in range(self.width):
                if (row, col) in self.moves:
                    output_row.append(self.nearby_mines((row, col))) # Discovered
                elif (row, col) in self.flags:
                    output_row.append(-1) # Flag
                elif self.game_over and (row, col) == self.death_square:
                    output_row.append(-2) # Death Square
                elif self.game_over and (row, col) in self.mines:
                    output_row.append(-3) # Bomb
                else:
                    output_row.append(-4) # Undiscovered
            output.append(output_row)
        return output
    
    def process_move(self, cell:tuple[int, int]) -> int:
        if cell in self.moves:
            if LOG: print("You have already moved to", cell)
        elif cell in self.mines:
            self.death_square = cell
            self.game_over = True
            if LOG: print("You have hit a mine")
        else:
            self.moves.add(cell)
        
        if self.game_over == False:
            return self.nearby_mines(cell)
        else:
            return None

    def nearby_cells(self, cell:tuple[int, int]) -> list[tuple[int, int]]:
        nearby_cells:list[tuple[int, int]] = []

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Add to cells if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    nearby_cells.append((i, j))
        return nearby_cells

    def nearby_mines(self, cell:tuple[int, int]):
        # Keep count of nearby mines
        count:int = 0
        
        for (i, j) in self.nearby_cells(cell):
            if (i, j) in self.mines:
                count += 1

        return count

    def won(self):
        return self.flags == self.mines and not self.game_over


class Sentence():
    def __init__(self, cells:set[tuple[int, int]], count:int):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other) -> bool:
        return self.cells == other.cells and self.count == other.count

    def __str__(self) -> str:
        return f"{self.cells} = {self.count}"
    
    def copy(self):
        return Sentence(self.cells.copy(), self.count)
    
    def risk(self) -> float:
        return float(10) if len(self.cells) == 0 else self.count / len(self.cells) # avoids division by zero


class MinesweeperAI():
    def __init__(self, game:Minesweeper):
        if LOG: print("Initializing AI...")

        self.game = game

        # Keep track of cells known to be safe or mines
        self.known_mines = set()
        self.known_safes = set()

        # List of sentences about the game known to be true
        self.knowledge:list[Sentence] = []
        if LOG: print("AI Initialized")

    # Non-performant needless code  
    # def mark_mine(self) -> bool:
    #     if self.known_mines:
    #         flag = self.known_mines.pop()
    #         self.game.flags.add(flag)
    #         if LOG: print("AI marking", flag, "as mine")
    #         return True
    #     else: return False

    def make_safe_move(self) -> tuple[int, int] | None:
        moves = []
        for safe in self.known_safes:
            if safe not in self.game.moves:
                moves.append(safe)

        try:
            move = moves[random.randrange(0, len(moves))]
            self.known_safes.remove(move)
            if LOG: print("AI moving safely to", move, "with options", moves)
            return move
        except ValueError:
            if LOG: print("AI could not find any valid safe move")
            return None
        
    def make_probable_move(self) -> tuple[int, int] | None:
        if len(self.knowledge) == 0: return None

        risky_sentances = sorted(self.knowledge, key=Sentence.risk)

        if risky_sentances[0].risk() < 0.5:
            move = risky_sentances[0].cells.copy().pop()
            if LOG: print("AI moving with probable safety to", move)
            return move
        else:
            return None

    def make_random_move(self) -> tuple[int, int] | None:
        attempts:int = 0
        while attempts < 256:
            attempts += 1
            i = random.randrange(0, self.game.height-1)
            j = random.randrange(0, self.game.width-1)
            if (i, j) not in self.game.moves and (i, j) not in self.known_mines:
                if LOG: print("AI Making random move to", (i, j))
                return (i, j)
        if LOG: print("AI could not find any valid random move")
        return None

    def add_knowledge(self, cell:tuple[int, int], count:int):
        if LOG: print("AI gaining knowledge: cell", cell, "has count", count)
        self.game.moves.add(cell)
        self.known_safes.add(cell)
        new_sentence = Sentence(self.game.nearby_cells(cell), count)
        self.knowledge.append(new_sentence)
        self.infer()
    
    def infer(self):
        if LOG: print("AI making inferences...")
        new_knowledge:list[Sentence] = []
        for sentence in self.knowledge.copy():
            if(len(sentence.cells) < 1): continue

            if LOG: print("  Making inferences from sentance", sentence)

            # Remove known cells
            sentence = self.trim(sentence)
            
            # Use multiple-sentance deduction
            for secondary_sentence in self.knowledge:
                if secondary_sentence == sentence: continue
                if sentence.cells.issubset(secondary_sentence.cells):
                    new_sentence_cells = secondary_sentence.cells - sentence.cells
                    new_sentence_count = secondary_sentence.count - sentence.count
                    new_sentence = self.trim(Sentence(new_sentence_cells, new_sentence_count))

                    if new_sentence not in new_knowledge:
                        if LOG: print("    Creating subset sentance:", new_sentence, "from", sentence, "and", secondary_sentence)
                        new_knowledge.append(new_sentence)
            
            if sentence.count == 0:
                if LOG: print("    All cells", sentence.cells, "are safe")
                for cell in sentence.cells.copy():
                    self.known_safes.add(cell)
            elif sentence.count == len(sentence.cells):
                if LOG: print("    All cells", sentence.cells, "are mines")
                for cell in sentence.cells:
                    self.known_mines.add(cell)
            elif sentence not in new_knowledge:
                new_knowledge.append(sentence)
        self.knowledge = new_knowledge

    def trim(self, sentence:Sentence) -> Sentence:
        new_sentence = sentence.copy()
        for cell in new_sentence.cells.copy():
            if cell in self.known_safes:
                new_sentence.cells.remove(cell)
                if LOG: print("    Creating subset sentance:", new_sentence, "from removal of safe cell", cell, "from", sentence)
            elif cell in self.known_mines:
                new_sentence.cells.remove(cell)
                new_sentence.count -= 1
                if LOG: print("    Creating subset sentance:", new_sentence, "from removal of mine", cell, "from", sentence)
        return new_sentence