import pygame
from game import Game
from board import Board

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_MARGIN = 20
BUTTON_TEXT_SIZE = 36

font = pygame.font.Font(None, 25)


def create_button(x, y, text):
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, WHITE, button_rect)

    text_surface = font.render(text, True, GRAY)
    text_rect = text_surface.get_rect(center=button_rect.center)

    screen.blit(text_surface, text_rect)

    return button_rect


# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Choose Difficulty")

difficulty_selected = None

button_easy = create_button(
    (SCREEN_WIDTH - BUTTON_WIDTH) / 2,
    SCREEN_HEIGHT / 2 - BUTTON_HEIGHT - BUTTON_MARGIN,
    "Easy"
)

button_medium = create_button(
    (SCREEN_WIDTH - BUTTON_WIDTH) / 2,
    SCREEN_HEIGHT / 2,
    "Medium"
)

button_hard = create_button(
    (SCREEN_WIDTH - BUTTON_WIDTH) / 2,
    SCREEN_HEIGHT / 2 + BUTTON_HEIGHT + BUTTON_MARGIN,
    "Hard"
)

# Main loop for difficulty selection
difficulty_selecting = True
while difficulty_selecting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            difficulty_selecting = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_easy.collidepoint(mouse_pos):
                difficulty_selected = 0  # Easy
                difficulty_selecting = False
            elif button_medium.collidepoint(mouse_pos):
                difficulty_selected = 1  # Medium
                difficulty_selecting = False
            elif button_hard.collidepoint(mouse_pos):
                difficulty_selected = 2  # Hard
                difficulty_selecting = False

    screen.fill(GRAY)

    # Draw buttons
    create_button(
        (SCREEN_WIDTH - BUTTON_WIDTH) / 2,
        SCREEN_HEIGHT / 2 - BUTTON_HEIGHT - BUTTON_MARGIN,
        "Easy"
    )

    create_button(
        (SCREEN_WIDTH - BUTTON_WIDTH) / 2,
        SCREEN_HEIGHT / 2,
        "Medium"
    )

    create_button(
        (SCREEN_WIDTH - BUTTON_WIDTH) / 2,
        SCREEN_HEIGHT / 2 + BUTTON_HEIGHT + BUTTON_MARGIN,
        "Hard"
    )

    pygame.display.flip()

# Easy: (9, 9) and 10 bombs... prob == .1
# Medium: (16, 16) and 32 bombs ... prob == .125
# Hard: (30, 16) and 60 ... prob == .125

if difficulty_selected == 0:
    size = (9, 9)
    prob = 0.1
elif difficulty_selected == 1:
    size = (16, 16)
    prob = 0.125
elif difficulty_selected == 2:
    size = (30, 16)
    prob = 0.125
else:
    print(f"difficulty selected: {difficulty_selected}")
    pygame.quit()

board = Board(size, prob)
screenSize = (board.getSize()[1] * 16 + 100, board.getSize()[0] * 16 + 100)

# Start the game
game = Game(board, screenSize)
game.run()
