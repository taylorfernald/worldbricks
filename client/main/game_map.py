import json
import math 
from constants import *
import pygame as pg
import random
from monsters import *
from resources import *
import monsters
from words import *
from table import Table

#Everything that goes on the map is put in this file. Also handles a class that represents the world
# (and can perform functions on it)

class Hex():
    # TODO: Change this from position based coordinates to an index based coordinates
    #       To find the position, use the index plus the map tile width
    def __init__(self, surface, color, outline_color, index):
        self.index = index #Where the hex is when it is put into a list
        self.surface = surface
        self.color = color
        self.outline_color = outline_color
        self.radius = TILE_WIDTH
        position = (index % MAP_SIZE[0], math.floor(index / MAP_SIZE[1]))
        self.position = (
            TILE_SCALE[0]+(position[0]*hex_distance*0.9), #How far each hex center is apart on the x axis
            TILE_SCALE[1]+
                (TILE_WIDTH*0.85*(position[0] % 2))+ #How far each other hex column is pushed down
                (position[1]*hex_distance))
        self.width = 1 # Width of outline
        self.token = None #The token that sits in the Hex
        self.decided = False #Whether the terrain is set in stone
    def draw(self):
        n, r = 6, self.radius
        x, y = self.position
        #Go ahead and calculate points so you don't have to do them twice
        points = [
            (x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n))
            for i in range(n)
        ]
        pg.draw.polygon(self.surface, self.color, points)
        pg.draw.polygon(self.surface, self.outline_color, points, self.width)

        if self.token: self.token.draw(self.surface)
    def toJSON(self):
        #The only two things that would be cared about are color. Position can be figured out later
        return '{"color": ' + str(list(self.color)) + ', "index": ' + str(self.index) + '}'
class Faction():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos #The hex where the faction headquarters
        #Go ahead and render the faction name
        self.nameReady = font.render(name, True, WHITE)
#Class for party marker
class Marker(pg.sprite.Sprite):
    def __init__(self, surface, Hex, image, name, group, camera):
        pg.sprite.Sprite.__init__(self, group)
        self.group = group
        self.surface = surface
        self.Hex = Hex #The hex the marker occupies.
        self.Hex.token = self
        self.image = image
        self.name = name
        self.nameImage = font.render(name, True, WHITE)
        w = self.Hex.radius
        self.rect = self.image.get_rect()
        self.rect.center = self.Hex.position
        self.faction = None
        self.camera = camera
    def setPosition(self, x, y):
        self.rect.center = (x, y)
    def setHex(self, Hex):
        self.Hex = Hex
        self.rect.center = self.Hex.position
    def getHex(self):
        return self.Hex
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft + self.camera.getOffset())
        #If the mouse is hovering over the marker, display its name
        screen.blit(self.nameImage, self.rect.center)
        #If the marker is a part of a faction, display its name
        if self.faction:
            screen.blit(self.faction.nameReady, self.rect.midtop)
    def toJSON(self):
        ### Each marker has a hex POSITION that it belongs to (position so we avoid circular references)
        return '{"position" : ' + str(list(self.getHex().position)) + ', "type" : "' + str(type(self).__name__) + '", "name": "' + str(self.name) + '"}'
class Settlement(Marker): #You can spend gold to generate a new dungeon
    def __init__(self, surface, Hex, image, name, group, camera):
        super().__init__(surface, Hex, image, name, group, camera)
    def generateNewDungeon(self, gold, Hexes):
        #Attempt to take away one gold point, then generate random lair on the map.
        #Returns the generated marker
        newHex = Hexes[0]
        while newHex.token:
            newHex = random.choice(Hexes)
        return Lair(self.surface, newHex, lair, "New Lair", self.group)
class Lair(Marker):
    def __init__(self, surface, Hex, name, group, camera):
        super().__init__(surface, Hex, lair, name, group, camera)
class Dungeon(Marker):
    def __init__(self, surface, Hex, name, group, camera):
        super().__init__(surface, Hex, dungeon, name, group, camera)
class Stronghold(Marker): #A player-made structure that can be attacked
    def __init__(self, surface, Hex, name, group, camera, type=0, numbers=1, money = 0):
        super().__init__(surface, Hex, stronghold, name + "'s Stronghold", group, camera)
        #Has a monster entry for the defender
        self.defender = DefenderList[type]
        self.numbers = numbers
        #Defeating the stronghold gives this much money.
        self.stash = money

#Camera goes here
class Camera():
    def __init__(self, index):
        #Which index to focus on
        self.index = index
    def getOffset(self):
        #Get the tuple position away from the origin (0, 0)
        return (0, 0)


class WorldMap():
    def __init__(self, screen):
        #Setup info
        self.screen = screen
        self.imax=MAP_SIZE[0]
        self.jmax=MAP_SIZE[1]
        self.hexes = []

        self.generate()

        self.locations = [] #A list of all locations. For checking every location
        self.imax, self.jmax = MAP_SIZE
        self.index = random.randint(0, (MAP_SIZE[0] * MAP_SIZE[1]) - 1) #where the party is rn
        self.camera = Camera(self.index)
        self.markerGroup = pg.sprite.Group()
        self.monsterList = Table(MonsterList)
    def loadMap(self, map):
        ###Using server hex information, create a hex map
        for hex in map['hexes']:
            self.hexes.append(Hex(self.screen, hex['color'], BLACK, hex['index']))
        for marker in map['markers']:
            Marker(self.screen, self.verifyRandomHex(), marker['type'], marker['name'], self.markerGroup, self.camera)
    
    def generate(self):
        #Make the map
        self.make_hex_map()
        startingHexIndex = random.randint(0, len(self.hexes)-1)
        self.runMountainsAlgorithm(self.hexes[startingHexIndex], startingHexIndex, 0, 1)
    def reset(self):
        #Generate wrapper that shows a warning beforehand.
        return self.generate()
    def make_hex_map(self):
        #Make the hex map; make each hex in the right position
        for i in range(MAP_SIZE[0] * MAP_SIZE[1]):
            self.hexes.append(Hex(self.screen, colors[-1], BLACK, i))

    def clamp(self, n, minn, maxn):
        if n < minn:
            return minn
        elif n > maxn:
            return maxn
        else:
            return n
    def grabNearbyHexes(self, iHex):
        #Given a position of a hex, return all of the surrounding hexes
        toFind = []
        scan = -self.imax-1
        for j in range(2):
            for i in range(2):
                scan += 1
                if scan + iHex > 0 and scan + iHex < len(self.hexes):
                    toFind.append(scan+iHex)
            scan += self.imax
        return toFind
    #Apply mountain algorithm
    def runMountainsAlgorithm(self, Hex, iHex, iColor, change):
        #Takes a Hex and chooses each hex that is around them, then runs the algorithm each Hex.
        if not Hex.decided:
            Hex.decided = True
            newIColor = self.clamp(random.randint(iColor-change, iColor+change), 0, len(colors)-1)
            Hex.color = colors[newIColor]
            nextHexes = self.grabNearbyHexes(iHex)
            for h in nextHexes:
                self.runMountainsAlgorithm(self.hexes[h], h, newIColor, change)
    def generateEncounter(self, Hex):
        if not Hex.token:
            #Use the monster table to make an encounter. Gives the encounter back.
            return self.monsterList.generateItem()
    def getRandomHex(self):
        ix = random.randint(0, self.imax-1)
        iy = random.randint(0, self.jmax-1)
        return self.hexes[self.jmax * iy + ix]
    def getHex(self, index):
        return self.hexes[index]
    def verifyRandomHex(self):
        current_hex = self.getRandomHex();
        while current_hex.token:
            current_hex = self.getRandomHex();
        return current_hex 
            
    def checkBoundaries(self, index, change):
        return (index+change) >= 0 and (index+change) < len(self.hexes)
    
    def getlen(self):
        return len(self.hexes)
    
    def draw(self):
        for Hex in self.hexes:
            Hex.draw()
    
    def placeStructure(self, structureClass, index=-1, setName=""):
        ###Given a structure type and other needed parameters, finds a place for it
        ###Returns structure if placed
        ###Prioritizes the index if one is given
        if index != -1: location = self.getHex(index)
        else: location = None

        checkedLocations = []
        #If there is no location, location has already been checked, or location is occupied
        #Choose another location
        #If we somehow go through all of the hexes on the map, then return False
        while not location or location in checkedLocations or location.token:
            location = self.getRandomHex()
            self.locations.append(location)
            if len(checkedLocations) == len(self.hexes): return False
        
        if setName == "": name = random.choice(Adjectives).capitalize() + " " + random.choice(Animals).capitalize()
        else: name = setName
        return structureClass(self.screen, location, name, self.markerGroup, self.camera)
    def toJSON(self):
        hexlist = ', '.join([hex.toJSON() for hex in self.hexes])
        markerGroup = ', '.join([marker.toJSON() for marker in self.markerGroup])
        ###Exports the class to JSON for network submission
        return '{"hexes": [' + hexlist + '], "markerGroup": [' + markerGroup + ']}'