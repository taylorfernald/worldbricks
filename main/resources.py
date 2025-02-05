#The goal of this file is to have all of the sprites in one place
import pygame as pg
from constants import *

#images are loaded here
def load_image(path, scale=TILE_SCALE):
    image = pg.image.load(path)
    return pg.transform.scale(image, scale)

house = load_image(IMAGES + "house.png")
lair = load_image(IMAGES + "lair.png")
dungeon = load_image(IMAGES + "dungeon.png")
party = load_image(IMAGES + "party.png")
UIBackground = load_image(IMAGES + "UIBackground.png")
#Icons
heart = load_image(TAGS + "heart.png", ICON_SIZE)
mirage = load_image(TAGS + "mirage.png", ICON_SIZE)
shield = load_image(TAGS + "shield.png", ICON_SIZE)
wing = load_image(TAGS + "wing.png", ICON_SIZE)
melee = load_image(TAGS + "melee.png", ICON_SIZE)
ranged = load_image(TAGS + "ranged.png", ICON_SIZE)
magic = load_image(TAGS + "magic.png", ICON_SIZE)

stronghold = load_image(IMAGES + "stronghold.png")

letter_to_tag = {
    'v':heart,
    'x':shield,
    'f':wing,
    'o':mirage,
    'm':melee,
    'r':ranged,
    's':magic
}

#Text portions for the tutorial pages
tutorial_pages = []
total_pages = 3
pages_path = "text/page"
for i in range(total_pages):
    f = open(pages_path+str(i)+".txt")
    tutorial_pages.append(f.readlines())
    #Cut off the newline for each line
    for j in range(len(tutorial_pages[-1])):
        tutorial_pages[-1][j] = tutorial_pages[-1][j][:-1]