class Tile:

    def __init__(self, tile_type):
        self.tile_type = tile_type

        self.attributes = {
            "floor": False,
            "blank": False,
            "water": False,
            "fire": False,
            "accelerate_left": False,
            "accelerate_right": False,
            "accelerate_down": False,
            "accelerate_up": False
        }

        # sets the tile's type
        if self.tile_type in self.attributes:
            self.attributes[self.tile_type] = True
        else:
            print(f"Invalid tile type: {self.tile_type}")
    
    def get_type(self):
        # returns the tile's type
        attr_list = list(self.attributes)
        for i in range(6): # number of attributes
            if attr_list[i] == self.tile_type:
                return attr_list[i]


