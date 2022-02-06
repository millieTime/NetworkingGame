import pickle
from network import SocketHandler

class SubObject:

    def __init__(self, number1, number2):
        self.num1 = number1
        self.num2 = number2

    def get_sum(self):
        return self.num1 + self.num2

    def get_num2(self):
        return self.num2

class TestObject:
    
    def __init__(self, number, name, sub_object):
        self.num = number
        self.name = name
        self.s_o = sub_object

    def get_so_sum(self):
        return self.s_o.get_sum()
    
    def get_name(self):
        return self.name

def main2():
    serverAddressPort   = ("192.168.137.1", 20001)

    # Create a UDP socket at client side
    s_hand = SocketHandler.SocketHandler(serverAddressPort)
    s_hand.send_to_server(pickle.dumps("opening UDP connection. . ."))
    s_hand.start()
    name = input("> ")

    sub_object = SubObject(5, 7)
    test_obj = TestObject(3, name, sub_object)
    pickled_obj = pickle.dumps(test_obj)
    s_hand.send_to_server(pickled_obj)
    #get new data
    while not s_hand.has_new_data:
        pass
    bytes_received = s_hand.get_data()
    #unpickle the data
    unpickled_list = pickle.loads(bytes_received)
    for index in range(len(unpickled_list)):
        unpickled_list[index] = pickle.loads(unpickled_list[index])
    for test_object in unpickled_list:
        if type(test_object) == str:
            print(test_object)
        else:
            print(test_object.get_name(), test_object.get_so_sum())

    name = input("> ")

    sub_object = SubObject(5, 7)
    test_obj = TestObject(3, name, sub_object)
    pickled_obj = pickle.dumps(test_obj)
    s_hand.send_to_server(pickled_obj)
    # get new data
    while not s_hand.has_new_data:
        pass
    bytes_received = s_hand.get_data()
    # unpickle the data
    unpickled_list = pickle.loads(bytes_received)
    for index in range(len(unpickled_list)):
        unpickled_list[index] = pickle.loads(unpickled_list[index])
    for test_object in unpickled_list:
        if type(test_object) == str:
            print(test_object)
        else:
            print(test_object.get_name(), test_object.get_so_sum())


######################## SETTING UP FOR THE GAME
from game import constants
from game.game_view import GameView
import arcade

def main():

    # start the game
    window = arcade.Window(constants.MAX_X, constants.MAX_Y,"Walking Game")
    window.game_view = GameView(window)
    window.show_view(window.game_view)
    arcade.run()

if __name__ == "__main__":
    main()
