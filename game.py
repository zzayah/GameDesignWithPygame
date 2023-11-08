import pygame as pg
import random

class Game:

    def __init__(self):
        self.screen_size = (306, 306) # images are 64 x 64 and spaces are 20 x 64 or 64 x 20 (counting borders)
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]

        self.won = False

        self.need_to_place_two = True

    def indices_of_zeros(self, direction):
        if direction == "up":
            fin_ary = [[] for _ in range(4)]  # Initialize a list for each column
            for col in range(4):
                for row in range(4):
                    if self.matrix[row][col] == 0:
                        fin_ary[col].append((row, col))  # Append coordinates of zero element
            return fin_ary
        if direction == "left":
            pass
        if direction == "right":
            pass
        if direction == "down":
            pass

    def draw(self):
        placed_two = False
        while_iterations = 0
        while not placed_two and self.need_to_place_two == True and while_iterations < 100:
            rand_idx_1 = random.randint(0, 3)
            rand_idx_2 = random.randint(0, 3)
            if self.matrix[rand_idx_1][rand_idx_2] == 0:
                self.matrix[rand_idx_1][rand_idx_2] = 2
                placed_two = True
                self.need_to_place_two = False
                
        for row in range(4):
            for col in range(4):
                # init sprite and resize
                sprite = pg.image.load(f"sprites/{self.matrix[row][col]}.png")
                sprite = pg.transform.scale(sprite, (64, 64))         

                # blit sprite
                self.screen.blit(sprite, ((10 + (74 * row)), (10 + (74 * col))))
    
    def run(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.screen.fill((187, 173, 160))
        pg.display.set_caption("2048")
        print(self.matrix)

        # game loop
        running = True
        while running:
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                keys = pg.key.get_pressed()
                if keys[pg.K_UP]:
                    idxs = self.indices_of_zeros("up")
                    for idx in idxs:
                        print(idx)
                    self.need_to_place_two = True

                elif keys[pg.K_LEFT]:
                    self.need_to_place_two = True

                elif keys[pg.K_RIGHT]:
                    self.need_to_place_two = True

                elif keys[pg.K_DOWN]:
                    self.need_to_place_two = True

                else:
                    print("no valid input detected")

            self.draw()
            pg.display.flip()
        pg.quit()


