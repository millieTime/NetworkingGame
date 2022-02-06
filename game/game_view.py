import arcade
import pickle
from game import constants
from game.player import Player, PlayerData
from network.SocketHandler import SocketHandler

class GameView(arcade.View):
    keys_down = {"left": False, "up": False, "down": False, "right": False}
    player = None
    on_call_players = {}

    def __init__(self, window):
        super().__init__()
        self.window = window
        for name in constants.PLAYER_NAMES:
            self.on_call_players[name] = Player(PlayerData(name))
        self.sock_hand = SocketHandler(constants.SERVER_ADDRESS_PORT)
        # Get a name
        self.sock_hand.send_to_server(pickle.dumps("Name Requested"))
        self.sock_hand.run_once()
        bytes_received = self.sock_hand.get_data()
        unpickled_received = pickle.loads(bytes_received)
        if unpickled_received not in constants.PLAYER_NAMES:
            print("Error: invalid response from server '", unpickled_received, "'")
            self.sock_hand.set_done(True)
            assert(False)
        else:
            print("Name received:", unpickled_received)
            self.player = Player(PlayerData(unpickled_received))
        self.sock_hand.start()

    def on_show(self):
        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
    
    def on_update(self, elapsed_time):
        if self.keys_down["left"] and not self.keys_down["right"]:
            self.player.move_left()
        elif self.keys_down["right"] and not self.keys_down["left"]:
            self.player.move_right()
        if self.keys_down["up"] and not self.keys_down["down"]:
            self.player.move_up()
        elif self.keys_down["down"] and not self.keys_down["up"]:
            self.player.move_down()

        pickled_obj = pickle.dumps(self.player.get_player_data())
        self.sock_hand.send_to_server(pickled_obj)


    def on_draw(self):
        # Check the socket handler to see where players
        # are at. Draw them to the screen.
        if self.sock_hand.has_new_data:
            received_bytes = self.sock_hand.get_data()
            received_list = pickle.loads(received_bytes)
            arcade.start_render()
            for index, player_bytes in enumerate(received_list):
                player = pickle.loads(player_bytes)
                if type(player) != str:
                    self.on_call_players[player.name].update_data(player)
                    self.on_call_players[player.name].draw()

    def on_key_press(self, symbol: int, modifiers: int):
        # handle input
        if symbol == arcade.key.UP:
            self.keys_down["up"] = True
        elif symbol == arcade.key.LEFT:
            self.keys_down["left"] = True
        elif symbol == arcade.key.RIGHT:
            self.keys_down["right"] = True
        elif symbol == arcade.key.DOWN:
            self.keys_down["down"] = True 
        return super().on_key_press(symbol, modifiers)
    
    def on_key_release(self, symbol: int, modifiers: int):
        # handle un-input
        if symbol == arcade.key.UP:
            self.keys_down["up"] = False
        elif symbol == arcade.key.LEFT:
            self.keys_down["left"] = False
        elif symbol == arcade.key.RIGHT:
            self.keys_down["right"] = False
        elif symbol == arcade.key.DOWN:
            self.keys_down["down"] = False
        return super().on_key_release(symbol, modifiers)

