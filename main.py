import csv
import pygame as pg
import tile
import copy

class Main:

    def __init__(self, filename):
        self.filename = filename
        self.board_names = []
        self.new_board = None
        self.board_tiles = None
        self.current_pos = []
        self.running = True
        self.first_turn = True  # Fix typo in the variable name

        self.alteration_right = 5
        self.alteration_down = 5

        self.sprite_sheet_pos = {
            "floor": (0, 0, 32, 32), # 0 x 0
            "player": (192, 448, 32, 32) # 6 x 14
        }

        self.screen = pg.display.set_mode((776, 616))


    def set_board(self):
        with open(f"{self.filename}.txt", "r") as ins:
            self.board_names = [[str(t) for t in line.split()] for line in ins]

        height = len(self.board_names)
        width = len(self.board_names[0])

        # Initialize new_board and board_tiles
        self.new_board = [["floor" for _ in range(width + 10)] for _ in range(height + 10)]
        self.board_tiles = [[tile.Tile("floor") for _ in range(width + 10)] for _ in range(height + 10)]

        for row in range(height):
            for col in range(width):
                self.new_board[row + 5][col + 5] = self.board_names[row][col]
                self.board_tiles[row + 5][col + 5] = tile.Tile(self.board_names[row][col])

    def draw(self):
        if self.first_turn:
            # tiles are 64 x 64 (= 576) and y coordinate gives 20 pixels of room
            self.screen.fill((255, 255, 255))
            self.first_turn = False

        for row in range(9):
            for col in range(9):
                cropped_image = None
                image_path = "ChipsSprites.png"
                tile_surf = pg.image.load(image_path)

                if self.new_board[row][col] == "player":
                    crop_rect = pg.Rect(self.sprite_sheet_pos["player"])
                    cropped_image = tile_surf.subsurface(crop_rect)
                elif self.new_board[row][col] == "floor":
                    crop_rect = pg.Rect(self.sprite_sheet_pos["floor"])
                    cropeed_image = tile_surf.subsurface(crop_rect)

                scaled_image = pg.transform.scale(cropped_image, (64, 64))
                self.screen.blit(scaled_image, (64 * col + 20, 64 * row + 20))

        # Update the display
        pg.display.flip()

    def run(self):
        pg.init()
        self.set_board()  # Call set_board before entering the game loop
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        if self.alteration_down == 5:
                            continue
                        elif self.alteration_down > 5:
                            self.alteration_down -= 1  # Fix direction
                        else:
                            print("self.alteration_down error")
                    elif event.key == pg.K_DOWN:
                        self.alteration_down += 1
                    elif event.key == pg.K_LEFT:
                        if self.alteration_right == 5:
                            continue
                        elif self.alteration_right > 5:
                            self.alteration_right -= 1  # Fix direction
                        else:
                            print("self.alteration_right error")
                    elif event.key == pg.K_RIGHT:
                        self.alteration_right += 1
            self.draw()

if __name__ == "__main__":
    Game = Main("CC")
    Game.run()
    pg.quit()  # Add pygame.quit() to ensure a clean exit
