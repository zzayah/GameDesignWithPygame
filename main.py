import pygame as pg
import random

class Main:
    def __init__(self, board_size):
        self.filename = "snake_sprites.png"

        # Ensure board_size is a tuple for consistency
        if not isinstance(board_size, tuple):
            board_size = (board_size, board_size)

        # PLAYER 1
        self.snake_pos = [[0 for _ in range(board_size[0])] for _ in range(board_size[1])]
        self.marker_ary = [["" for _ in range(board_size[0])] for _ in range(board_size[1])]
        self.snake_pos[int(board_size[1]/4)][1] = ((int(board_size[0]/4), 1), "right")
        self.snake_pos[int(board_size[1]/4)][2] = ((int(board_size[0]/4), 2), "right")
        self.snake_pos[int(board_size[1]/4)][3] = ((int(board_size[0]/4), 3), "right")
        self.snake_head = ((int(board_size[0]/4), 3), "right")
        self.input_direction = "right"
        self.snake_length = 3 
        self.old_time = 0
        self.new_time = 0
        self.event_occured = False

        # PLAYER 2
        self.p2_snake_pos = [[0 for _ in range(board_size[0])] for _ in range(board_size[1])]
        self.p2_marker_ary = [["" for _ in range(board_size[0])] for _ in range(board_size[1])]
        self.p2_snake_pos[3*int(board_size[1]/4)][1] = ((3*int(board_size[0]/4), 1), "right")
        self.p2_snake_pos[3*int(board_size[1]/4)][2] = ((3*int(board_size[0]/4), 2), "right")
        self.p2_snake_pos[3*int(board_size[1]/4)][3] = ((3*int(board_size[0]/4), 3), "right")
        self.p2_snake_head = ((3*int(board_size[0]/4), 3), "right")
        self.p2_input_direction = "right"
        self.p2_snake_length = 3
        self.p2_new_time = 0
        self.p2_old_time = 0
        self.p2_event_occured = False

        # FRUIT
        self.fruit_location = (int(2*board_size[0]/3), int(board_size[1]/2))

        # LOSE/WIN
        self.lost = False
        self.won = False
        self.filled = False
        self.lost_message = ""

        # COLORS - Assuming you have these images in your project directory
        self.green2 = pg.image.load("green2.png")
        self.green1 = pg.image.load("green1.png")
        self.red = pg.image.load("red.png")
        self.blue = pg.image.load("blue.png")
        self.gold = pg.image.load("gold.png")

        # OPTIMIZATION AND BOOTUP
        self.startup_flip_executed = False
        self.check_fruit_iter = 0

        # BOARD
        self.board_size = board_size
        if not (10 < self.board_size[0] < 26) or not (10 < self.board_size[1] < 26):
            print("invalid board_size input")
            pg.quit()
        self.screen = pg.display.set_mode(((self.board_size[0]*64)+40, (self.board_size[1]*64)+40))

    def init_set_board(self):
        # Blit tiles in checkerboard pattern and initial positions for snakes and fruit
        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                tile = self.green2 if (i + j) % 2 == 0 else self.green1
                self.screen.blit(tile, ((j*64)+20, (i*64)+20))

        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                if self.snake_pos[i][j] != 0:
                    self.screen.blit(self.red, ((j * 64 + 20), (i * 64 + 20)))
                if self.p2_snake_pos[i][j] != 0:
                    self.screen.blit(self.blue, ((j * 64 + 20), (i * 64 + 20)))
        
        self.screen.blit(self.gold, ((self.fruit_location[0] * 64 + 20), (self.fruit_location[1] * 64 + 20)))

    def do_periodic(self):
        if self.check_snakes_overlap():
            self.lost_message = "Collision! Hash out who wins!"
            self.lost = True
            return
        # Blit tiles in checkerboard pattern
        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                if (i + j) % 2 == 0:
                    self.screen.blit(self.green2, ((j*64)+20, (i*64)+20))
                else:
                    self.screen.blit(self.green1, ((j*64)+20, (i*64)+20))
        
        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                if self.snake_pos[i][j] != 0:
                    self.screen.blit(self.red, ((j * 64 + 20), (i * 64 + 20)))

        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                if self.p2_snake_pos[i][j] != 0:
                    self.screen.blit(self.blue, ((j * 64 + 20), (i * 64 + 20)))


    
    def handle_input(self):
        new_ary = [[0 for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]

        # Iterate over each cell in the board
        for d in range(self.board_size[1]):
            for r in range(self.board_size[0]):
                # Check if there's a snake part at this position
                if self.snake_pos[r][d] != 0:
                    pos, current_direction = self.snake_pos[r][d]                    
                    new_direction = self.marker_ary[pos[0]][pos[1]]
                    # Update direction based on the marker
                    if new_direction == "left" and current_direction != "right":
                        current_direction = "left"
                    elif new_direction == "right" and current_direction != "left":
                        current_direction = "right"
                    elif new_direction == "up" and current_direction != "down":
                        current_direction = "up"
                    elif new_direction == "down" and current_direction != "up":
                        current_direction = "down"
                        
                    # Update snake position with the new direction
                    match(current_direction):
                        case "left":
                            pos = (pos[0], pos[1] - 1)
                        case "right":
                            pos = (pos[0], pos[1] + 1)
                        case "up":
                            pos = (pos[0] - 1, pos[1])
                        case "down":
                            pos = (pos[0] + 1, pos[1])
                        case _:
                            print("error")
                            break

                    if pos[0] < 0 or pos[0] >= self.board_size[1] or pos[1] < 0 or pos[1] >= self.board_size[0]:
                        self.lost_message = "Player 1 hit the wall!"
                        self.lost = True
                        return  # Exit the method to avoid further processing

                    new_ary[pos[0]][pos[1]] = (pos, current_direction)

        self.snake_pos = new_ary

    def p2_handle_input(self):
        new_p2_ary = [[0 for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]

        for d in range(self.board_size[1]):
            for r in range(self.board_size[0]):
                if self.p2_snake_pos[r][d] != 0:
                    pos, current_direction = self.p2_snake_pos[r][d]                    
                    new_direction = self.p2_marker_ary[pos[0]][pos[1]]
                    if new_direction == "left" and current_direction != "right":
                        current_direction = "left"
                    elif new_direction == "right" and current_direction != "left":
                        current_direction = "right"
                    elif new_direction == "up" and current_direction != "down":
                        current_direction = "up"
                    elif new_direction == "down" and current_direction != "up":
                        current_direction = "down"
                        
                    match(current_direction):
                        case "left":
                            pos = (pos[0], pos[1] - 1)
                        case "right":
                            pos = (pos[0], pos[1] + 1)
                        case "up":
                            pos = (pos[0] - 1, pos[1])
                        case "down":
                            pos = (pos[0] + 1, pos[1])
                        case _:
                            print("error")
                            break

                    if pos[0] < 0 or pos[0] >= self.board_size[1] or pos[1] < 0 or pos[1] >= self.board_size[0]:
                        self.lost_message = "Player 2 hit the wall!"
                        self.lost = True
                        return

                    new_p2_ary[pos[0]][pos[1]] = (pos, current_direction)

        self.p2_snake_pos = new_p2_ary

    def check_fruit(self):
        # Flag to check if the fruit is inside the snake
        fruit_inside_snake = False

        # Iterate over the entire snake_pos array
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                # Check if the current cell is part of the snake
                if self.snake_pos[row][col] != 0 and self.p2_snake_pos[row][col] != 0:
                    # Check if the fruit is in the same position as this part of the snake
                    if (col, row) == self.fruit_location:
                        fruit_inside_snake = True
                        break  # No need to check further if we've found the fruit inside the snake

            if fruit_inside_snake:
                break

        # If the fruit is inside the snake, relocate it
        if fruit_inside_snake:
            self.place_fruit()  # This will find a new location for the fruit

    def place_fruit(self):
        if self.fruit_location is None:
            while True:
                i = random.randint(3, self.board_size[1] - 4)
                j = random.randint(3, self.board_size[0] - 4)
                if self.snake_pos[i][j] == 0 and self.marker_ary[i][j] == "" and self.p2_snake_pos[i][j] == 0 and self.p2_marker_ary[i][j] == "":
                    self.fruit_location = (i, j)
                    break
        if self.fruit_location is not None:
            self.screen.blit(self.gold, ((self.fruit_location[0] * 64 + 20), (self.fruit_location[1] * 64 + 20)))

    def lost_screen(self):
        if not self.filled:
            transparent_white = pg.Surface((self.board_size[0]*64+40, self.board_size[1]*64+40), pg.SRCALPHA)
            transparent_white.fill((255, 255, 255, 128))
            self.screen.blit(transparent_white, (0, 0))
            self.filled = True
        
        font = pg.font.Font(None, 80)
        text = font.render(self.lost_message, True, (0, 0, 0))
        
        # Calculate the position to center the text
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        
        # Blit the text onto the screen
        self.screen.blit(text, text_rect)

    def check_snakes_overlap(self):
        # Iterate over the entire snake_pos array of player 1
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                # Check if the current cell is part of the snake
                if self.snake_pos[row][col] != 0:
                    # Check if player 2's snake occupies the same position
                    if self.p2_snake_pos[row][col] != 0:
                        return True  # Snakes are overlapping
        return False  # Snakes are not overlapping

    def run(self):
        pg.init()
        pg.display.set_caption("Snake")
        self.screen.fill((87, 138, 52))
        running = True
        self.init_set_board()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            if self.lost == True:
                self.lost_screen()
                pg.display.flip()
            else:
                self.check_fruit()

                self.new_time = pg.time.get_ticks()
                self.p2_new_time = pg.time.get_ticks()

                self.event_occured = self.new_time - 500 > self.old_time
                self.p2_event_occured = self.p2_new_time - 500 > self.p2_old_time

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == pg.KEYDOWN:
                        if not self.event_occured:
                            if event.key == pg.K_UP and self.snake_head[1] != "down":
                                self.input_direction = "up"
                            elif event.key == pg.K_DOWN and self.snake_head[1] != "up":
                                self.input_direction = "down"
                            elif event.key == pg.K_LEFT and self.snake_head[1] != "right":
                                self.input_direction = "left"
                            elif event.key == pg.K_RIGHT and self.snake_head[1] != "left":
                                self.input_direction = "right"
                        if not self.p2_event_occured:
                            if event.key == pg.K_s and self.p2_snake_head[1] != "down":
                                self.p2_input_direction = "down"
                            elif event.key == pg.K_w and self.p2_snake_head[1] != "up":
                                self.p2_input_direction = "up"
                            elif event.key == pg.K_a and self.p2_snake_head[1] != "right":
                                self.p2_input_direction = "left"
                            elif event.key == pg.K_d and self.p2_snake_head[1] != "left":
                                self.p2_input_direction = "right"

                if self.event_occured and not self.lost and not self.won:

                    # P1 CHECK IF LOST
                    if self.snake_head[0][0] < 0 or self.snake_head[0][0] >= self.board_size[1] or self.snake_head[0][1] < 0 or self.snake_head[0][1] >= self.board_size[0]:
                        self.lost = True
                        
                    # P1 CHECK IF WON
                    if self.snake_length == self.board_size[0] * self.board_size[1]:
                        self.won = True

                    # P1 HANDLE INPUT
                    if self.input_direction == "left" and self.snake_head[1] != "right":
                        if self.snake_head[1] == "left" and self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]-1] != 0:
                            self.lost_message = "Player 1 hit themselves!"
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] - 1), "left")
                        self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]+1] = self.snake_head[1]
                    elif self.input_direction == "right" and self.snake_head[1] != "left":
                        if self.snake_pos[1] == "right" and self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]+1] != 0:
                            self.lost_message = "Player 1 hit themselves!"
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] + 1), "right")
                        self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]-1] = self.snake_head[1]
                    elif self.input_direction == "up" and self.snake_head[1] != "down":
                        if self.snake_head[1] == "up" and self.snake_pos[self.snake_head[0][0]-1][self.snake_head[0][1]] != 0:
                            self.lost_message = "Player 1 hit themselves!"
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0] - 1, self.snake_head[0][1]), "up")
                        self.marker_ary[self.snake_head[0][0]+1][self.snake_head[0][1]] = self.snake_head[1]
                    elif self.input_direction == "down" and self.snake_head[1] != "up":
                        try:
                            if (self.snake_head[1] == "down" and self.snake_pos[self.snake_head[0][0]+1][self.snake_head[0][1]] != 0):
                                self.lost_message = "Player 1 hit themselves!"
                                self.lost = True
                        except IndexError:
                            self.lost_message = "Player 1 hit themselves!"
                            self.lost = True
                        self.snake_head = ((self.snake_head[0][0] + 1, self.snake_head[0][1]), "down")                    
                        self.marker_ary[self.snake_head[0][0]-1][self.snake_head[0][1]] = self.snake_head[1]

                    if self.fruit_location != None and self.snake_head[0] == (self.fruit_location[1], self.fruit_location[0]):
                        match(self.snake_head[1]):
                            case "right":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "right")
                                self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] + 1), "right")
                                self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]-1] = self.snake_head[1]
                            case "left":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "left")
                                self.snake_head = ((self.snake_head[0][0], self.snake_head[0][1] - 1), "left")
                                self.marker_ary[self.snake_head[0][0]][self.snake_head[0][1]+1] = self.snake_head[1]
                            case "up":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "up")
                                self.snake_head = ((self.snake_head[0][0] - 1, self.snake_head[0][1]), "up")
                                self.marker_ary[self.snake_head[0][0]+1][self.snake_head[0][1]] = self.snake_head[1]
                            case "down":
                                self.snake_pos[self.snake_head[0][0]][self.snake_head[0][1]] = (self.snake_head[0], "down")
                                self.snake_head = ((self.snake_head[0][0] + 1, self.snake_head[0][1]), "down")
                                self.marker_ary[self.snake_head[0][0]-1][self.snake_head[0][1]] = self.snake_head[1]
                        self.snake_length += 1
                        self.fruit_location = None
                    self.handle_input()
                    self.old_time = self.new_time

                if self.p2_event_occured and not self.lost and not self.won:
                    # P2 CHECK IF LOST
                    if self.p2_snake_head[0][0] < 0 or self.p2_snake_head[0][0] >= self.board_size[1] or self.p2_snake_head[0][1] < 0 or self.p2_snake_head[0][1] >= self.board_size[0]:
                        self.lost_message = "Player 2 hit the wall!"
                        self.lost = True
                    # P2 CHECK IF WON
                    if self.p2_snake_length == self.board_size[0] * self.board_size[1]:
                        self.won = True
                    # P2 HANDLE INPUT
                    if self.p2_input_direction == "left" and self.p2_snake_head[1] != "right":
                        if self.p2_snake_head[1] == "left" and self.p2_snake_pos[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]-1] != 0:
                            self.lost_message = "Player 2 hit themselves!"
                            self.lost = True
                        self.p2_snake_head = ((self.p2_snake_head[0][0], self.p2_snake_head[0][1] - 1), "left")
                        self.p2_marker_ary[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]+1] = self.p2_snake_head[1]
                    elif self.p2_input_direction == "right" and self.p2_snake_head[1] != "left":
                        
                        if self.p2_snake_pos[1] == "right" and self.p2_snake_pos[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]+1] != 0:
                            self.lost_message = "Player 2 hit themselves!"
                            self.lost = True
                        self.p2_snake_head = ((self.p2_snake_head[0][0], self.p2_snake_head[0][1] + 1), "right")
                        self.p2_marker_ary[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]-1] = self.p2_snake_head[1]
                    elif self.p2_input_direction == "up" and self.p2_snake_head[1] != "down":
                        if self.p2_snake_head[1] == "up" and self.p2_snake_pos[self.p2_snake_head[0][0]-1][self.p2_snake_head[0][1]] != 0:
                            self.lost_message = "Player 2 hit themselves!"
                            self.lost = True
                        self.p2_snake_head = ((self.p2_snake_head[0][0] - 1, self.p2_snake_head[0][1]), "up")
                        self.p2_marker_ary[self.p2_snake_head[0][0]+1][self.p2_snake_head[0][1]] = self.p2_snake_head[1]
                    elif self.p2_input_direction == "down" and self.p2_snake_head[1] != "up":
                        try:
                            if (self.p2_snake_head[1] == "down" and self.p2_snake_pos[self.p2_snake_head[0][0]+1][self.p2_snake_head[0][1]] != 0):
                                self.lost_message = "Player 2 hit themselves!"
                                self.lost = True
                        except IndexError:
                            self.lost_message = "Player 2 hit themselves!"
                            self.lost = True
                        self.p2_snake_head = ((self.p2_snake_head[0][0] + 1, self.p2_snake_head[0][1]), "down")                    
                        self.p2_marker_ary[self.p2_snake_head[0][0]-1][self.p2_snake_head[0][1]] = self.p2_snake_head[1]

                    if self.fruit_location != None and self.p2_snake_head[0] == (self.fruit_location[1], self.fruit_location[0]):
                        match(self.p2_snake_head[1]):
                            case "right":
                                self.p2_snake_pos[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]] = (self.p2_snake_head[0], "right")
                                self.p2_snake_head = ((self.p2_snake_head[0][0], self.p2_snake_head[0][1] + 1), "right")
                                self.p2_marker_ary[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]-1] = self.p2_snake_head[1]
                            case "left":
                                self.p2_snake_pos[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]] = (self.p2_snake_head[0], "left")
                                self.p2_snake_head = ((self.p2_snake_head[0][0], self.p2_snake_head[0][1] - 1), "left")
                                self.p2_marker_ary[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]+1] = self.p2_snake_head[1]
                            case "up":
                                self.p2_snake_pos[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]] = (self.p2_snake_head[0], "up")
                                self.p2_snake_head = ((self.p2_snake_head[0][0] - 1, self.p2_snake_head[0][1]), "up")
                                self.p2_marker_ary[self.p2_snake_head[0][0]+1][self.p2_snake_head[0][1]] = self.p2_snake_head[1]
                            case "down":
                                self.p2_snake_pos[self.p2_snake_head[0][0]][self.p2_snake_head[0][1]] = (self.p2_snake_head[0], "down")
                                self.p2_snake_head = ((self.p2_snake_head[0][0] + 1, self.p2_snake_head[0][1]), "down")
                                self.p2_marker_ary[self.p2_snake_head[0][0]-1][self.p2_snake_head[0][1]] = self.p2_snake_head[1]
                        self.p2_snake_length += 1
                        self.fruit_location = None
                    self.p2_handle_input()    
                    self.p2_old_time = self.p2_new_time            
                    
                    self.startup_flip_executed = True
                    self.do_periodic()
                    self.place_fruit()
                    pg.display.flip()

                if not self.startup_flip_executed:
                    pg.display.flip()
            
        pg.quit()

main = Main((13))
main.run()
