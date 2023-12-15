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
        self.current_pos = [[None for _ in range(9)] for _ in range(9)]  # Initialize current_pos list

        self.running = True
        self.first_turn = True  # Fix typo in the variable name

        self.alteration_right = 4
        self.alteration_down = 4

        self.sprite_sheet_pos = {
            "floor": (0, 0, 32, 32), # 0 x 0
            "player": (64, 448, 32, 32), # 6 x 14
            "solid": (0, 32, 32, 32), # 0 x 1
            "water": (0, 96, 32, 32),
            "chip": (0, 64, 32, 32)
        }

        self.screen = pg.display.set_mode((776, 616))


    def set_board(self):
        with open(f"{self.filename}.txt", "r") as ins:
            self.board_names = [[str(t) for t in line.split()] for line in ins]

        height = len(self.board_names)
        width = len(self.board_names[0])

        # Initialize new_board and board_tiles
        self.new_board = [["floor" for _ in range(width + 8)] for _ in range(height + 8)]
        self.board_tiles = [[tile.Tile("floor") for _ in range(width + 8)] for _ in range(height + 8)]

        for row in range(height):
            for col in range(width):
                self.new_board[row + 4][col + 4] = self.board_names[row][col]
                self.board_tiles[row + 4][col + 4] = tile.Tile(self.board_names[row][col])
        
        for row in range(len(self.board_tiles)):
            for col in range(len(self.board_tiles[0])):
                if self.board_tiles[row][col].get_type() == "player":
                    self.alteration_down = row
                    self.alteration_right = col
                    self.board_tiles[row][col] = tile.Tile("floor")

    def draw(self):
        if self.first_turn:
            # tiles are 64 x 64 (= 576) and y coordinate gives 20 pixels of room
            self.screen.fill((255, 255, 255))
            self.first_turn = False
        
        for row in range(9):
            for col in range(9):
                self.current_pos[row][col] = self.board_tiles[row+self.alteration_down-4][col+self.alteration_right-4]
        # set player in the middle
        # self.current_pos[4][4] = tile.Tile("player")

        for row in range(9):
            for col in range(9):
                image_path = "ChipsSprites.png"
                tile_surf = pg.image.load(image_path)
                current_tile = self.current_pos[row][col].get_type()
                crop_rect = pg.Rect(self.sprite_sheet_pos[current_tile])
                cropped_image = tile_surf.subsurface(crop_rect)
                scaled_image = pg.transform.scale(cropped_image, (64, 64))
                self.screen.blit(scaled_image, (64 * col + 20, 64 * row + 20))

        # blit player on top of the board
        player_image_path = "ChipsSprites (4).png"
        player_tile_surf = pg.image.load(player_image_path)
        player_crop_rect = pg.Rect(self.sprite_sheet_pos["player"])
        cropped_player = player_tile_surf.subsurface(player_crop_rect)
        scaled_player = pg.transform.scale(cropped_player, (64, 64))
        scaled_player.set_colorkey((255, 255, 255))
        self.screen.blit(scaled_player, ((64 * 4 + 20), (64 * 4 + 20)))

        # Update the display
        pg.display.flip()

    def run(self):
        pg.init()
        pg.display.set_caption("Chip's Challenge")
        self.set_board()  # Call set_board before entering the game loop
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        if self.alteration_down > 4 and self.alteration_down <= len(self.board_tiles[0])-4:
                            if self.board_tiles[self.alteration_down-1][self.alteration_right].get_type() == "solid":
                                print("solid in the way")
                                break
                            else:
                                self.alteration_down -= 1
                        else:
                            print("self.alteration_down error. (pg.K_UP)")
                    elif event.key == pg.K_DOWN:
                        if self.alteration_down < len(self.board_tiles[0])-5:
                            if self.board_tiles[self.alteration_down+1][self.alteration_right].get_type() == "solid":
                                print("solid in the way")
                                break
                            else:
                                self.alteration_down += 1
                        else:
                            print("self.alteration_down error. (pg.K_DOWN)")
                    elif event.key == pg.K_LEFT:
                        if self.alteration_right > 4 and self.alteration_right <= len(self.board_tiles)-4:
                            if self.board_tiles[self.alteration_down][self.alteration_right-1].get_type() == "solid":
                                print("solid in the way")
                                break
                            else:
                                self.alteration_right -= 1
                        else:
                            print("self.alteration_right error. (pg.K_LEFT)")
                    elif event.key == pg.K_RIGHT:
                        if self.alteration_right < len(self.board_tiles)-5:
                            if self.board_tiles[self.alteration_down][self.alteration_right+1].get_type() == "solid":
                                print("solid in the way")
                                break
                            else:
                                self.alteration_right += 1
                        else:
                            print("self.alteration_right error. (K_RIGHT)")
            self.draw()

if __name__ == "__main__":
    Game = Main("CC")
    Game.run()
    pg.quit()
