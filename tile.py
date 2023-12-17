class Tile:

    def __init__(self, tile_type):
        self.tile_type = tile_type

        self.attributes = {
            "solid": False,
            "wboot": False,
            "player": False,
            "floor": False,
            "chip": False,
            "red_k": False,
            "red_d": False,
            "info": False,
            "water": False,
            "fire": False,
            "acc_ri": False,
            "acc_le": False,
            "accelerate_down": False,
            "accelerate_up": False
        }

        self.attributes[self.tile_type] = True
    
    def get_type(self):
        # returns the tile's type
        return self.tile_type
