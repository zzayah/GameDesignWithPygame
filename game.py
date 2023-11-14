import pygame as pg
import random
import copy

class Game:

    def __init__(self):
        self.screen_size = (306, 356)
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        self.prev_board = copy.deepcopy(self.matrix)
        self.first_turn = True

        self.won = False
        self.lost = False
        self.score = 0
        self.prev_score = 0

        self.need_to_place_two = True

        self.clock = pg.time.Clock()

    def merge_tiles(self, direc, bool = None):

        if bool:

            check_against = copy.deepcopy(self.matrix)

            merged = [[False for _ in range(4)] for _ in range(4)]
            if direc == 'left':
                for i in range(4):
                    for j in range(4):
                        shift = 0
                        if i > 0:
                            for q in range(i):
                                if check_against[q][j] == 0:
                                    shift += 1
                            if shift > 0:
                                check_against[i - shift][j] = check_against[i][j]
                                check_against[i][j] = 0
                            if check_against[i - shift - 1][j] == check_against[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                                check_against[i - shift - 1][j] *= 2
                                check_against[i - shift][j] = 0
                                merged[i - shift - 1][j] = True

            elif direc == 'right':
                for i in range(3):
                    for j in range(4):
                        shift = 0
                        for q in range(i + 1):
                            if check_against[3 - q][j] == 0:
                                shift += 1
                        if shift > 0:
                            check_against[2 - i + shift][j] = check_against[2 - i][j]
                            check_against[2 - i][j] = 0
                        if 3 - i + shift <= 3:
                            if check_against[2 - i + shift][j] == check_against[3 - i + shift][j] and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
                                check_against[3 - i + shift][j] *= 2
                                check_against[2 - i + shift][j] = 0
                                merged[3 - i + shift][j] = True

            elif direc == 'up':
                for i in range(4):
                    for j in range(4):
                        shift = 0
                        for q in range(j):
                            if check_against[i][q] == 0:
                                shift += 1
                        if shift > 0:
                            check_against[i][j - shift] = check_against[i][j]
                            check_against[i][j] = 0
                        if check_against[i][j - shift] == check_against[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                            check_against[i][j - shift - 1] *= 2
                            check_against[i][j - shift] = 0
                            merged[i][j - shift - 1] = True

            elif direc == 'down':
                for i in range(4):
                    for j in range(4):
                        shift = 0
                        for q in range(j):
                            if check_against[i][3 - q] == 0:
                                shift += 1
                        if shift > 0:
                            check_against[i][3 - j + shift] = check_against[i][3 - j]
                            check_against[i][3 - j] = 0
                        if 4 - j + shift <= 3:
                            if check_against[i][4 - j + shift] == check_against[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
                                check_against[i][4 - j + shift] *= 2
                                check_against[i][3 - j + shift] = 0
                                merged[i][4 - j + shift] = True

            return check_against
        
        else:

            if not direc == "undo":
                self.prev_score = copy.deepcopy(self.score)
                self.prev_board = copy.deepcopy(self.matrix)

            merged = [[False for _ in range(4)] for _ in range(4)]
            if direc == 'left':
                for i in range(4):
                    for j in range(4):
                        shift = 0
                        if i > 0:
                            for q in range(i):
                                if self.matrix[q][j] == 0:
                                    shift += 1
                            if shift > 0:
                                self.matrix[i - shift][j] = self.matrix[i][j]
                                self.matrix[i][j] = 0
                            if self.matrix[i - shift - 1][j] == self.matrix[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                                self.matrix[i - shift - 1][j] *= 2
                                self.score += self.matrix[i - shift - 1][j]
                                self.matrix[i - shift][j] = 0
                                merged[i - shift - 1][j] = True

            elif direc == 'right':
                for i in range(3):
                    for j in range(4):
                        shift = 0
                        for q in range(i + 1):
                            if self.matrix[3 - q][j] == 0:
                                shift += 1
                        if shift > 0:
                            self.matrix[2 - i + shift][j] = self.matrix[2 - i][j]
                            self.matrix[2 - i][j] = 0
                        if 3 - i + shift <= 3:
                            if self.matrix[2 - i + shift][j] == self.matrix[3 - i + shift][j] and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
                                self.matrix[3 - i + shift][j] *= 2
                                self.score += self.matrix[3 - i + shift][j]
                                self.matrix[2 - i + shift][j] = 0
                                merged[3 - i + shift][j] = True

            elif direc == 'up':
                for i in range(4):
                    for j in range(4):
                        shift = 0
                        for q in range(j):
                            if self.matrix[i][q] == 0:
                                shift += 1
                        if shift > 0:
                            self.matrix[i][j - shift] = self.matrix[i][j]
                            self.matrix[i][j] = 0
                        if self.matrix[i][j - shift] == self.matrix[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                            self.matrix[i][j - shift - 1] *= 2
                            self.score += self.matrix[i][j - shift - 1]
                            self.matrix[i][j - shift] = 0
                            merged[i][j - shift - 1] = True

            elif direc == 'down':
                for i in range(4):
                    for j in range(4):
                        shift = 0
                        for q in range(j):
                            if self.matrix[i][3 - q] == 0:
                                shift += 1
                        if shift > 0:
                            self.matrix[i][3 - j + shift] = self.matrix[i][3 - j]
                            self.matrix[i][3 - j] = 0
                        if 4 - j + shift <= 3:
                            if self.matrix[i][4 - j + shift] == self.matrix[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
                                self.matrix[i][4 - j + shift] *= 2
                                self.score += self.matrix[i][4 - j + shift]
                                self.matrix[i][3 - j + shift] = 0
                                merged[i][4 - j + shift] = True
                                
            elif direc == "undo":
                self.score = self.prev_score
                self.matrix = copy.deepcopy(self.prev_board)

            return self.matrix

    def check_won_or_lost(self):
        zeros_exist = False
        for row in range(4):
            for col in range(4):
                if self.matrix[row][col] == 0:
                    zeros_exist = True
                if self.matrix[row][col] == 2048:
                    self.won = True

        if not self.first_turn and not zeros_exist:
            # Check if no move results in a change
            current_board = copy.deepcopy(self.matrix)
            moves = ['up', 'down', 'left', 'right']
            no_change = all(current_board == self.merge_tiles(move) for move in moves)
            if no_change:
                self.lost = True

    def draw(self):
        if self.won:
            # self.screen.fill((255, 215, 0)) <----------- commented to test functionality (working)
            font = pg.font.Font(None, 80)
            text = font.render("YOU WON!", True, (0, 0, 0))
            text_rect = text.get_rect()
            self.screen.blit(text, (((self.screen.get_width() - text_rect.width) / 2), 113))

            font = pg.font.Font(None, 30)
            text = font.render(f"Score: {self.score}", True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(text, (20, 316))
            return

        elif self.lost:
            # self.screen.fill((0, 0, 0)) <------- commented to test functionality (working)
            font = pg.font.Font(None, 80)
            text = font.render("YOU LOST!", True, (255, 255, 255))
            text_rect = text.get_rect()
            self.screen.blit(text, (((self.screen.get_width() - text_rect.width) / 2), 113))

            font = pg.font.Font(None, 30)
            text = font.render(f"Score: {self.score}", True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(text, (20, 316))
            return

        font = pg.font.Font(None, 30)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0), (255, 255, 255, 255))
        self.screen.blit(text, (20, 316))

        placed_two = False
        while_iterations = 0
        while not placed_two and self.need_to_place_two and while_iterations < 100:
            rand_idx_1 = random.randint(0, 3)
            rand_idx_2 = random.randint(0, 3)
            if self.matrix[rand_idx_1][rand_idx_2] == 0:
                chance_to_place_2 = random.random()
                if self.first_turn:
                    self.matrix[rand_idx_1][rand_idx_2] = 2
                    self.first_turn = False
                elif chance_to_place_2 <= 0.5:
                    self.matrix[rand_idx_1][rand_idx_2] = 2
                else:
                    self.matrix[rand_idx_1][rand_idx_2] = 4
                placed_two = True
                self.need_to_place_two = False

        for row in range(4):
            for col in range(4):
                sprite = pg.image.load(f"sprites/{self.matrix[row][col]}.png")
                sprite = pg.transform.scale(sprite, (64, 64))
                self.screen.blit(sprite, ((10 + (74 * row)), (10 + (74 * col))))

    def run(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.screen.fill((187, 173, 160))
        pg.display.set_caption("2048")
        print(self.matrix)

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                    
                keys = pg.key.get_pressed()
                if self.won or self.lost:
                    break
                elif keys[pg.K_ESCAPE]:
                    self.merge_tiles("undo")
                    print("undo move")
                elif keys[pg.K_UP]:
                    self.merge_tiles("up")
                    self.need_to_place_two = True
                elif keys[pg.K_LEFT]:
                    self.merge_tiles("left")
                    self.need_to_place_two = True
                elif keys[pg.K_RIGHT]:
                    self.merge_tiles("right")
                    self.need_to_place_two = True
                elif keys[pg.K_DOWN]:
                    self.merge_tiles("down")
                    self.need_to_place_two = True
                else:
                    print("no_imp")

            self.check_won_or_lost()
            self.draw()
            pg.display.flip()
        pg.quit()
