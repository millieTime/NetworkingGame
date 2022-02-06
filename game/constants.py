from pathlib import Path

DIR = Path(__file__).resolve().parent
#This is the path we're looking for
DIRROOT = str(DIR.resolve().parent)

MAX_X = 500
MAX_Y = 500

PLAYER_NAMES = ["black", "blue", "yellow", "red", "cyan", "purple", "green"]

PLAYER_IMAGES = {
    "black": DIRROOT + "/images/player_black.png",
    "blue": DIRROOT + "/images/player_blue.png",
    "cyan": DIRROOT + "/images/player_cyan.png",
    "green": DIRROOT + "/images/player_green.png",
    "purple": DIRROOT + "/images/player_purple.png",
    "red": DIRROOT + "/images/player_red.png",
    "yellow": DIRROOT + "/images/player_yellow.png"
}

SERVER_ADDRESS_PORT   = ("10.244.133.8", 20001) # windows .133.8
