import pygame as pg
import tile
import math

class Main:

    def __init__(self, filename):
        self.filename = filename
        self.board_names = []
        self.new_board = None
        self.board_tiles = None
        self.current_pos = [[None for _ in range(9)] for _ in range(9)]  # Initialize current_pos list

        self.running = True
        self.first_turn = True
        
        self.lost = False
        self.won = False

        self.amt_chips = 0

        self.sound_played = False

        self.alteration_right = 4
        self.alteration_down = 4

        # for enemy movement
        self.prev_time = 0
        self.time_now = 0
        self.altered_enemy_location = None
        self.enemy_location = None

        # Green Checkered and Button
        self.gc_location = None

        self.inventory = [["floor" for _ in range(4)] for _ in range(2)]

        self.sprite_sheet_pos = {
            "floor": (0, 0, 32, 32), # 0 x 0
            "player": (64, 448, 32, 32), # 3 x 14
            "solid": (0, 32, 32, 32), # 0 x 1
            "water": (0, 96, 32, 32),
            "chip": (0, 64, 32, 32),
            "wboot": (192, 256, 32, 32), # 6 x 8
            "acc_ri": (32, 96, 32, 32),
            "acc_le": (32, 128, 32, 32),
            "red_k": (192, 160, 32, 32),
            "red_d": (32, 224, 32, 32),
            "info": (64, 480, 32, 32),
            "pad": (96, 320, 32, 32),
            "enemy": (192, 0, 32, 32),
            "dirt": (32, 0, 32, 32),
            "wdirt": (32, 448, 32, 32),
            "g_butt": (64, 96, 32, 32),
            "gc_flo": (64, 192, 32, 32),
            "gc_sol": (64, 160, 32, 32),
            "bara": (64, 64, 32, 32),
            "bara_b": (64, 320, 32, 32),
            "fire": (0, 128, 32, 32),
            "gboot": (192, 352, 32, 32),
            "stain": (160, 384, 32, 32)
        }

        self.time = None
        self.screen = pg.display.set_mode((776, 616))

    def set_board(self):
        with open(f"{self.filename}.txt", "r") as ins:
            self.board_names = [[str(t) for t in line.split()] for line in ins]

        height = len(self.board_names)
        width = len(self.board_names[0])

        # create 4 space boarder around the entire map
        self.new_board = [["floor" for _ in range(width + 8)] for _ in range(height + 8)]

        # set all text to tile objects
        self.board_tiles = [[tile.Tile("floor") for _ in range(width + 8)] for _ in range(height + 8)]

        for row in range(height):
            for col in range(width):
                self.new_board[row + 4][col + 4] = self.board_names[row][col]
                self.board_tiles[row + 4][col + 4] = tile.Tile(self.board_names[row][col])
        
        for row in range(len(self.board_tiles)):
            for col in range(len(self.board_tiles[0])):
                eval_against = self.board_tiles[row][col].get_type()
                if eval_against == "player":
                    self.alteration_down = row
                    self.alteration_right = col
                    self.board_tiles[row][col] = tile.Tile("floor")
                elif eval_against == "enemy":
                    self.enemy_location = (row, col) # y, x
                    self.altered_enemy_location = (row, col)
                elif eval_against == "gc_sol":
                    self.gc_location = (row, col) # y, x
        

    def draw(self):
        if self.lost:
            self.screen.fill((0, 0, 0))
            font = pg.font.Font(None, 70)
            game_over_txt = font.render("GAME OVER", True, (255, 255, 255))
            text_rect = game_over_txt.get_rect()
            text_rect.center = (776//2, 616//2)
            self.screen.blit(game_over_txt, text_rect)
            pg.display.flip()
        elif self.won:
            self.screen.fill((255, 255, 255))
            font = pg.font.Font(None, 70)
            game_over_txt = font.render("YOU WIN!", True, (0, 0, 0))
            text_rect = game_over_txt.get_rect()
            text_rect.center = (776//2, 616//2)
            self.screen.blit(game_over_txt, text_rect)
            pg.display.flip()
        else:
            if self.first_turn:
                # tiles are 64 x 64 (= 576) and y coordinate gives 20 pixels of room
                self.screen.fill((255, 255, 255))
                self.first_turn = False
                font = pg.font.Font(None, 50)
                time_txt = font.render("Time:", True, (0, 0, 0))
                time_rect = time_txt.get_rect()
                time_rect.center = (686, 100)
                self.screen.blit(time_txt, time_rect)

                chip_count_txt = font.render("Chips:", True, (0, 0, 0))
                chip_rect = chip_count_txt.get_rect()
                chip_rect.center = (686, 200)
                self.screen.blit(chip_count_txt, chip_rect)

            self.amt_chips = 0
            for row in range(2):
                for col in range(4):
                    if self.inventory[row][col] == "chip":
                        self.amt_chips += 1
            
            font = pg.font.Font(None, 50)
            chip_ct_txt = font.render(f"{self.amt_chips}", True, (0, 0, 0))
            chip_ct_rect = chip_ct_txt.get_rect()
            chip_ct_rect.center = (686, 250)
            chip_ct_white_rec = pg.Surface((50, 50))
            chip_ct_white_rec.fill((255, 255, 255))
            self.screen.blit(chip_ct_white_rec, chip_ct_rect)
            self.screen.blit(chip_ct_txt, chip_ct_rect)

            
            # clock
            clock_txt = font.render(f"{60-self.time//1000}", True, (0, 0, 0))
            clock_rect = clock_txt.get_rect()
            clock_rect.center = (686, 150)
            white_rec = pg.Surface((50, 50))
            white_rec.fill((255, 255, 255))
            self.screen.blit(white_rec, clock_rect)
            self.screen.blit(clock_txt, clock_rect)

            for row in range(2):
                for col in range(4):
                    item_image_path = "ChipsSprites (3).png"
                    item_tile_surf = pg.image.load(item_image_path)
                    item_crop_rect = pg.Rect(self.sprite_sheet_pos[self.inventory[row][col]])
                    cropped_item = item_tile_surf.subsurface(item_crop_rect)
                    scaled_item = pg.transform.scale(cropped_item, (64, 64))
                    self.screen.blit(scaled_item, ((row * 64 + (576+46)), (col* 64 + (320+20))))
            
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
        pg.mixer.init()
        pg.display.set_caption("Chip's Challenge")
        pg.mixer.music.load("background_msc.mp3")
        pg.mixer.music.set_volume(.3)
        pg.mixer.music.play(-1)
        self.set_board()  # Call set_board before entering the game loop
        while self.running:
            self.time = pg.time.get_ticks()

            if self.won:
                if not self.sound_played:
                    pg.mixer.music.stop()
                    win_sound = pg.mixer.Sound("win.mp3")
                    win_sound.set_volume(.3)
                    win_sound.play()
                    self.sound_played = True

            if 60-(self.time//1000) < 0 or self.lost and not self.won:
                self.lost = True
                if not self.sound_played:
                    pg.mixer.music.stop()
                    lose_sound = pg.mixer.Sound("lose.mp3")
                    lose_sound.set_volume(0.3)
                    lose_sound.play()
                    self.sound_played = True
            
            # enemy movement
            if math.floor((self.time)//1000) > self.prev_time:
                self.prev_time = math.floor((self.time//1000))
                if self.altered_enemy_location == self.enemy_location:
                    el_y = self.enemy_location[0]
                    el_x = self.enemy_location[1]
                    self.board_tiles[el_y][el_x] = tile.Tile("floor")
                    self.board_tiles[el_y+1][el_x] = tile.Tile("enemy")
                    self.enemy_location = (el_y+1, el_x)
                elif self.altered_enemy_location != self.enemy_location:
                    el_y = self.enemy_location[0]
                    el_x = self.enemy_location[1]
                    self.board_tiles[el_y][el_x] = tile.Tile("floor")
                    self.board_tiles[el_y-1][el_x] = tile.Tile("enemy")
                    self.enemy_location = (el_y-1, el_x)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN and not self.lost:
                    if event.key == pg.K_UP:
                        check_against = self.board_tiles[self.alteration_down-1][self.alteration_right].get_type()
                        if self.alteration_down > 4 and self.alteration_down <= len(self.board_tiles[0])-4:
                            if check_against == "solid":
                                break
                            elif check_against == "wboot":
                                self.board_tiles[self.alteration_down-1][self.alteration_right] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "wboot"
                                        self.alteration_down -= 1
                                        break
                            elif check_against == "chip":
                                self.board_tiles[self.alteration_down-1][self.alteration_right] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "chip"
                                        self.alteration_down -= 1
                                        break
                            elif check_against == "red_k":
                                self.board_tiles[self.alteration_down-1][self.alteration_right] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "red_k"
                                        self.alteration_down -= 1
                                        break
                            elif check_against == "red_d":
                                for row in self.inventory:
                                    if "red_k" in row:
                                        row[row.index("red_k")] = "floor"
                                        self.alteration_down -= 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "water" and not (any("wboot" in row for row in self.inventory)):
                                self.lost = True
                                print("You are not Jesus. Next time, don't try to walk on water without Flippers. Game over.")
                            elif check_against == "info":
                                if self.filename == "level_one":
                                    print("Level 1: Obtain the 4 chips located around the map by gathering the Red Key and Flippers and traversing through movement tiles.")
                                elif self.filename == "level_two":
                                    print("welcome to level 2.")                                
                                self.alteration_down -= 1
                            elif check_against == "pad":
                                if self.amt_chips == 4:
                                    self.alteration_down -= 1
                                    self.won = True
                            elif check_against == "enemy" or check_against == "fire":
                                self.lost = True
                            elif check_against == "stain":
                                has_boots = False
                                for row in self.inventory:
                                    if "gboot" in row:
                                        has_boots = True
                                        self.alteration_down -= 2
                                        break
                                if not has_boots:
                                    self.lost = True
                            elif check_against == "gboot":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "gboot"
                                        self.alteration_down -= 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "gc_sol":
                                break
                            elif check_against == "g_butt":
                                if self.board_tiles[self.gc_location[0]][self.gc_location[1]].get_type() == "gc_sol":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_flo")
                                elif self.board_tiles[self.gc_location[0]][self.gc_location[1]] == "gc_flo":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_sol")
                                self.alteration_down -= 1
                            elif check_against == "dirt":
                                check_against_against = self.board_tiles[self.alteration_down-2][self.alteration_right].get_type()
                                if check_against_against == "water":
                                    self.board_tiles[self.alteration_down-2][self.alteration_right] = tile.Tile("wdirt")
                                    self.board_tiles[self.alteration_down-1][self.alteration_right] = tile.Tile("floor")
                                    self.alteration_down -= 1
                                elif check_against_against == "floor":
                                    self.board_tiles[self.alteration_down-2][self.alteration_right] = tile.Tile("dirt")
                                    self.board_tiles[self.alteration_down-1][self.alteration_right] = tile.Tile("floor")
                                    self.alteration_down -= 1
                                elif check_against_against == "enemy":
                                    print("Congrats, you found a part of the code I thought wouldn't be necessary. How about you do what you're supposed to with the dirt?")
                                elif check_against_against == "solid":
                                    break
                            elif check_against == "bara_b":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "bara_b"
                                        self.alteration_down -= 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "bara":
                                for row in self.inventory:
                                    if "bara_b" in row:
                                        row[row.index("bara_b")] = "floor"
                                        self.alteration_down -= 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            else:
                                self.alteration_down -= 1
                        else:
                            print("self.alteration_down error. (pg.K_UP)")
                    elif event.key == pg.K_DOWN:
                        check_against = self.board_tiles[self.alteration_down+1][self.alteration_right].get_type()
                        if self.alteration_down < len(self.board_tiles[0])-5:
                            if check_against == "solid":
                                break
                            elif check_against == "wboot":
                                self.board_tiles[self.alteration_down+1][self.alteration_right] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "wboot"
                                        self.alteration_down += 1
                                        break
                            elif check_against == "chip":
                                self.board_tiles[self.alteration_down+1][self.alteration_right] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "chip"
                                        self.alteration_down += 1
                                        break
                            elif check_against == "red_k":
                                self.board_tiles[self.alteration_down+1][self.alteration_right] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "red_k"
                                        self.alteration_down += 1
                                        break
                            elif check_against == "red_d":
                                for row in self.inventory:
                                    if "red_k" in row:
                                        row[row.index("red_k")] = "floor"
                                        self.alteration_down += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "water" and not (any("wboot" in row for row in self.inventory)):
                                self.lost = True
                                print("You are not Jesus. Next time, don't try to walk on water without Flippers. Game over.")
                            elif check_against == "info":
                                if self.filename == "level_one":
                                    print("Level 1: Obtain the 4 chips located around the map by gathering the Red Key and Flippers and traversing through movement tiles.")
                                elif self.filename == "level_two":
                                    print("welcome to level 2.")                                
                                self.alteration_down += 1
                            elif check_against == "pad":
                                if self.amt_chips == 4:
                                    self.alteration_down += 1
                                    self.won = True
                            elif check_against == "enemy" or check_against == "fire":
                                self.lost = True
                            elif check_against == "stain":
                                has_boots = False
                                for row in self.inventory:
                                    if "gboot" in row:
                                        has_boots = True
                                        self.alteration_down += 2
                                        break
                                if not has_boots:
                                    self.lost = True
                            elif check_against == "gboot":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "gboot"
                                        self.alteration_down += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "gc_sol":
                                break
                            elif check_against == "g_butt":
                                if self.board_tiles[self.gc_location[0]][self.gc_location[1]].get_type() == "gc_sol":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_flo")
                                elif self.board_tiles[self.gc_location[0]][self.gc_location[1]] == "gc_flo":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_sol")
                                self.alteration_down += 1
                            elif check_against == "dirt":
                                check_against_against = self.board_tiles[self.alteration_down+2][self.alteration_right].get_type()
                                if check_against_against == "water":
                                    self.board_tiles[self.alteration_down+2][self.alteration_right] = tile.Tile("wdirt")
                                    self.board_tiles[self.alteration_down+1][self.alteration_right] = tile.Tile("floor")
                                    self.alteration_down += 1
                                elif check_against_against == "floor":
                                    self.board_tiles[self.alteration_down+2][self.alteration_right] = tile.Tile("dirt")
                                    self.board_tiles[self.alteration_down+1][self.alteration_right] = tile.Tile("floor")
                                    self.alteration_down += 1
                                elif check_against_against == "enemy":
                                    print("Congrats, you found a part of the code I thought wouldn't be necessary. How about you do what you're supposed to with the dirt?")
                                elif check_against_against == "solid":
                                    break
                            elif check_against == "bara_b":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "bara_b"
                                        self.alteration_down += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "bara":
                                for row in self.inventory:
                                    if "bara_b" in row:
                                        row[row.index("bara_b")] = "floor"
                                        self.alteration_down += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            else:
                                self.alteration_down += 1
                        else:
                            print("self.alteration_down error. (pg.K_DOWN)")
                    elif event.key == pg.K_LEFT:
                        check_against = self.board_tiles[self.alteration_down][self.alteration_right-1].get_type()
                        if self.alteration_right > 4 and self.alteration_right <= len(self.board_tiles)-4:
                            if check_against == "solid":
                                break
                            elif check_against == "wboot":
                                self.board_tiles[self.alteration_down][self.alteration_right-1] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "wboot"
                                        self.alteration_right -= 1
                                        break
                            elif check_against == "chip":
                                self.board_tiles[self.alteration_down][self.alteration_right-1] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "chip"
                                        self.alteration_right -= 1
                                        break
                            elif check_against == "red_k":
                                self.board_tiles[self.alteration_down][self.alteration_right-1] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "red_k"
                                        self.alteration_right -= 1
                                        break
                            elif check_against == "red_d":
                                for row in self.inventory:
                                    if "red_k" in row:
                                        row[row.index("red_k")] = "floor"
                                        self.alteration_right -= 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "water" and not (any("wboot" in row for row in self.inventory)):
                                self.lost = True
                                print("You are not Jesus. Next time, don't try to walk on water without Flippers. Game over.")
                            elif check_against == "info":
                                if self.filename == "level_one":
                                    print("Level 1: Obtain the 4 chips located around the map by gathering the Red Key and Flippers and traversing through movement tiles.")
                                elif self.filename == "level_two":
                                    print("welcome to level 2.")
                                self.alteration_right -= 1
                            elif check_against == "acc_le":
                                self.alteration_right -= 2
                                break
                            elif check_against == "acc_ri":
                                break
                            elif check_against == "pad":
                                if self.amt_chips == 4:
                                    self.alteration_right -= 1
                                    self.won = True
                            elif check_against == "enemy" or check_against == "fire":
                                self.lost = True
                            elif check_against == "stain":
                                has_boots = False
                                for row in self.inventory:
                                    if "gboot" in row:
                                        has_boots = True
                                        self.alteration_right -= 2
                                        break
                                if not has_boots:
                                    self.lost = True
                            elif check_against == "gboot":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "gboot"
                                        self.alteration_right -= 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "gc_sol":
                                break
                            elif check_against == "g_butt":
                                if self.board_tiles[self.gc_location[0]][self.gc_location[1]].get_type() == "gc_sol":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_flo")
                                elif self.board_tiles[self.gc_location[0]][self.gc_location[1]] == "gc_flo":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_sol")
                                self.alteration_right -= 1
                            elif check_against == "dirt":
                                check_against_against = self.board_tiles[self.alteration_down][self.alteration_right-2].get_type()
                                if check_against_against == "water":
                                    self.board_tiles[self.alteration_down][self.alteration_right-2] = tile.Tile("wdirt")
                                    self.board_tiles[self.alteration_down][self.alteration_right-1] = tile.Tile("floor")
                                    self.alteration_right -= 1
                                elif check_against_against == "floor":
                                    self.board_tiles[self.alteration_down][self.alteration_right-2] = tile.Tile("dirt")
                                    self.board_tiles[self.alteration_down][self.alteration_right-1] = tile.Tile("floor")
                                    self.alteration_right -= 1
                                elif check_against_against == "enemy":
                                    print("Congrats, you found a part of the code I thought wouldn't be necessary. How about you do what you're supposed to with the dirt?")
                                elif check_against_against == "solid":
                                    break
                            elif check_against == "bara_b":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "bara_b"
                                        self.alteration_right -= 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "bara":
                                for row in self.inventory:
                                    if "bara_b" in row:
                                        row[row.index("bara_b")] = "floor"
                                        self.board_tiles[self.alteration_down][self.alteration_right-1] = tile.Tile("floor")
                                        self.alteration_right -= 1
                                        break
                            else:
                                self.alteration_right -= 1
                        else:
                            print("self.alteration_right error. (pg.K_LEFT)")
                    elif event.key == pg.K_RIGHT:
                        check_against = self.board_tiles[self.alteration_down][self.alteration_right+1].get_type()
                        if self.alteration_right < len(self.board_tiles)-5:
                            if check_against == "solid":
                                break
                            elif check_against == "wboot":
                                self.board_tiles[self.alteration_down][self.alteration_right+1] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "wboot"
                                        self.alteration_right += 1
                                        break
                            elif check_against == "chip":
                                self.board_tiles[self.alteration_down][self.alteration_right+1] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "chip"
                                        self.alteration_right += 1
                                        break
                            elif check_against == "red_k":
                                self.board_tiles[self.alteration_down][self.alteration_right+1] = tile.Tile("floor")
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "red_k"
                                        self.alteration_right += 1
                                        break
                            elif check_against == "red_d":
                                for row in self.inventory:
                                    if "red_k" in row:
                                        row[row.index("red_k")] = "floor"
                                        self.alteration_right += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right+1] = tile.Tile("floor")
                                        break
                            elif check_against == "water" and not (any("wboot" in row for row in self.inventory)):
                                self.lost = True
                                print("You are not Jesus. Next time, don't try to walk on water. Game over.")
                            elif check_against == "info":
                                if self.filename == "level_one":
                                    print("Level 1: Obtain the 4 chips located around the map by gathering the Red Key and Flippers and traversing through movement tiles.")
                                elif self.filename == "level_two":
                                    print("welcome to level 2.")
                                self.alteration_right += 1
                            elif check_against == "acc_le":
                                break
                            elif check_against == "acc_ri":
                                self.alteration_right += 2
                                break
                            elif check_against == "pad":
                                if self.amt_chips == 4:
                                    self.alteration_right += 1
                                    self.won = True
                            elif check_against == "enemy" or check_against == "fire":
                                self.lost = True
                            elif check_against == "stain":
                                has_boots = False
                                for row in self.inventory:
                                    if "gboot" in row:
                                        has_boots = True
                                        self.alteration_right += 2
                                        break
                                if not has_boots:
                                    self.lost = True
                            elif check_against == "gboot":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "gboot"
                                        self.alteration_right += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "gc_sol":
                                break
                            elif check_against == "g_butt":
                                if self.board_tiles[self.gc_location[0]][self.gc_location[1]].get_type() == "gc_sol":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_flo")
                                elif self.board_tiles[self.gc_location[0]][self.gc_location[1]] == "gc_flo":
                                    self.board_tiles[self.gc_location[0]][self.gc_location[1]] = tile.Tile("gc_sol")
                                self.alteration_right += 1
                            elif check_against == "dirt":
                                check_against_against = self.board_tiles[self.alteration_down][self.alteration_right+2].get_type()
                                if check_against_against == "water":
                                    self.board_tiles[self.alteration_down][self.alteration_right+2] = tile.Tile("wdirt")
                                    self.board_tiles[self.alteration_down][self.alteration_right+1] = tile.Tile("floor")
                                    self.alteration_right += 1
                                elif check_against_against == "floor":
                                    self.board_tiles[self.alteration_down][self.alteration_right+2] = tile.Tile("dirt")
                                    self.board_tiles[self.alteration_down][self.alteration_right+1] = tile.Tile("floor")
                                    self.alteration_right += 1
                                elif check_against_against == "enemy":
                                    print("Congrats, you found a part of the code I thought wouldn't be necessary. How about you do what you're supposed to with the dirt?")
                                elif check_against_against == "solid":
                                    break
                            elif check_against == "bara_b":
                                for row in self.inventory:
                                    if "floor" in row:
                                        row[row.index("floor")] = "bara_b"
                                        self.alteration_right += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            elif check_against == "bara":
                                for row in self.inventory:
                                    if "bara_b" in row:
                                        row[row.index("bara_b")] = "floor"
                                        self.alteration_right += 1
                                        self.board_tiles[self.alteration_down][self.alteration_right] = tile.Tile("floor")
                                        break
                            else:
                                self.alteration_right += 1
                        else:
                            print("self.alteration_right error. (K_RIGHT)")
            self.draw()

if __name__ == "__main__":
    Game = Main("level_two")
    Game.run()
    pg.quit()
