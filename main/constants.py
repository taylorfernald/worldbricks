import pygame as pg
from enum import Enum
#All of the constants that we need
(width, height) = (920, 720)
SKY_BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
grass_color = (100, 255, 100)
forest_color = (0, 150, 0)
mountain_color = (255, 150, 150)
hill_color = (255, 200, 200)
beach_color = (242,210,169)
water_color = (100, 100, 255)
IMAGES = "images/"
TAGS = "images/tags/"

#Size stuff
TILE_WIDTH = 50
ICON_SIZE = (16, 16)
TILE_SCALE = (TILE_WIDTH, TILE_WIDTH)
MAP_SIZE = (12, 8)
hex_distance = TILE_WIDTH * 1.7 #Distance between each hex center

pg.init()
font = pg.font.SysFont('comic_sans', round(TILE_WIDTH / 2))

colors = [mountain_color, hill_color, forest_color, grass_color, beach_color, water_color]

#Gameplay Variables
gold = 4
rations = 4
max_rations = 4
torches = 4
max_torches = 4
hirelings = 0
max_hirelings = 4

#Connection Information
server_url = "https://localhost"

#states / screens
class MainStates(Enum):
    HEXCRAWL = 1
    BATTLE = 2
    TUTORIAL = 3
    TITLE = 4
    USERNAME = 5
    PASSWORD = 6
    LOADING = 7