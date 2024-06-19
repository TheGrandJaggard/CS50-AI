import pygame
import sys
import time

from minesweeper_lib import Minesweeper, MinesweeperAI, SPECS

# Board size
SIZE = "medium"
# Whether to show instructions
INSTRUCTIONS = False

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
window_size = window_width, window_height = 600, 400
screen = pygame.display.set_mode(window_size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * window_width) - (BOARD_PADDING * 2)
board_height = window_height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / SPECS[SIZE][1], board_height / SPECS[SIZE][0]))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(SIZE)
ai = MinesweeperAI(game)

# Show instructions initially
instructions = INSTRUCTIONS

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((window_width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for row, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((window_width / 2), 150 + 30 * row)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((window_width / 4), (3 / 4) * window_height, window_width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    raw_board = game.get_board()
    visual_cells = []
    for row in range(len(raw_board)):
        visual_row = []
        for col in range(len(raw_board[0])):
            raw_cell = raw_board[row][col]

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + col * cell_size,
                board_origin[1] + row * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Set cell content
            if raw_cell == -1: # Flag
                screen.blit(flag, rect)
            elif raw_cell == -2 or raw_cell == -3: # Bomb
                screen.blit(mine, rect)
            elif raw_cell == -4: # Undiscovered
                pass
            else: # Discovered
                neighbors = smallFont.render(str(raw_cell), True, BLACK)
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            visual_row.append(rect)
        visual_cells.append(visual_row)

    # Random Move button
    randomMoveButton = pygame.Rect(
        (2 / 3) * window_width, BOARD_PADDING,
        (window_width / 3) - BOARD_PADDING, 50
    )
    buttonText = mediumFont.render("Rand. Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = randomMoveButton.center
    pygame.draw.rect(screen, WHITE, randomMoveButton)
    screen.blit(buttonText, buttonRect)

    # All moves button
    allMovesButton = pygame.Rect(
        (2 / 3) * window_width, BOARD_PADDING + 70,
        (window_width / 3) - BOARD_PADDING, 50
    )
    buttonText = mediumFont.render("All Moves", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = allMovesButton.center
    pygame.draw.rect(screen, WHITE, allMovesButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * window_width, BOARD_PADDING + 140,
        (window_width / 3) - BOARD_PADDING, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # Display text
    text = "Lost" if game.game_over else "Won" if game.mines == game.flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * window_width, (2 / 3) * window_height)
    screen.blit(text, textRect)

    (left, _, right) = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()

    # Check for a right-click to toggle flagging
    if right and not game.game_over:
        for row in range(game.height):
            for col in range(game.width):
                if (visual_cells[row][col].collidepoint(mouse)
                        and (row, col) not in game.moves):
                    if (row, col) in game.flags:
                        game.flags.remove((row, col))
                        ai.known_mines.remove((row, col))
                    else:
                        game.flags.add((row, col))
                        ai.known_mines.add((row, col))
                    time.sleep(0.2)

    if left:
        # If AI button clicked, make an AI move
        if randomMoveButton.collidepoint(mouse):
            move = ai.make_safe_move()
            if move == None:
                move = ai.make_probable_move()
            if move == None:
                move = ai.make_random_move()
            if move == None:
                continue
            count = game.process_move(move)
            if count != None: ai.add_knowledge(move, count)
            time.sleep(0.2)
        
        elif allMovesButton.collidepoint(mouse):
            while True:
                if game.game_over: print("Somehow I lost making a safe move"); break
                move = ai.make_safe_move()
                if move == None: break
                count = game.process_move(move)
                if count != None: ai.add_knowledge(move, count)
            time.sleep(0.2)

        # Reset game state
        elif resetButton.collidepoint(mouse):
            print("Reset button clicked")
            game = Minesweeper(SIZE)
            ai = MinesweeperAI(game)
            continue

        # User-made move
        elif not game.game_over:
            for row in range(game.height):
                for col in range(game.width):
                    if (visual_cells[row][col].collidepoint(mouse)
                            and (row, col) not in game.flags
                            and (row, col) not in game.moves):
                        move = (row, col)
                        count = game.process_move(move)
                        if count != None: ai.add_knowledge(move, count)

    pygame.display.flip()