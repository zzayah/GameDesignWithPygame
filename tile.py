class Tile:

    def __init__(self):
        self.board = []
        self.current_pos = []
        self.water = False
        self.accelerate_left = False
        self.accelerate_right = False
        self.accelerate_up = False
        self.accelerate_down = False
    
    def set_board(self):
        
