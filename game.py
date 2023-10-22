import pygame as pg

class Game:

    def __init__(self):
        self.screen_size = (306, 306) # images are 64 x 64 and spaces are 20 x 64 or 64 x 20 (counting borders)
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]

    def draw(self):
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

            self.draw()
            pg.display.flip()
        pg.quit()


