import arcade
from game import constants

class PlayerData:
    def __init__(self, name, x = -1, y = -1):
        self.name = name
        if x < 0:
            x = constants.MAX_X / 2
        if y < 0:
            y = constants.MAX_Y / 2
        self.center_x = x
        self.center_y = y

class Player(arcade.Sprite):

    def __init__(self, player_data):
        super().__init__(constants.PLAYER_IMAGES[player_data.name])
        self.name = player_data.name
        self.update_data(player_data)
        
    def get_player_data(self):
        return PlayerData(self.name, self.center_x, self.center_y)
    
    def update_data(self, player_data):
        self.center_x = player_data.center_x
        self.center_y = player_data.center_y

    def get_name(self):
        return self.name

    def move_left(self):
        if self.center_x > 0:
            self.center_x -= 1
    
    def move_right(self):
        if self.center_x < constants.MAX_X:
            self.center_x += 1

    def move_up(self):
        if self.center_y < constants.MAX_Y:
            self.center_y += 1
    
    def move_down(self):
        if self.center_y > 0:
            self.center_y -= 1
