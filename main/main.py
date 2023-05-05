import pygame as pg
import math
import random
from table import Table as tb
from monsters import MonsterList
from creatures import *
from explore import *
from words import *

pg.init()
(width, height) = (920, 720)
screen = pg.display.set_mode((width, height))
pg.display.set_caption("World Bricks")
SKY_BLUE = (100, 100, 255)
background_color = SKY_BLUE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
grass_color = (100, 255, 100)
forest_color = (0, 150, 0)
mountain_color = (255, 150, 150)
hill_color = (255, 200, 200)
beach_color = (242,210,169)
water_color = (100, 100, 255)
screen.fill(background_color)
#images are loaded here
house = pg.image.load("../images/house.png")
lair = pg.image.load("../images/lair.png")
dungeon = pg.image.load("../images/dungeon.png")
party = pg.image.load("../images/party.png")
UIBackground = pg.image.load("../images/UIBackground.png")
UIBackground.set_alpha(128)
house_ready = pg.transform.scale(house, (50, 50))
lair_ready = pg.transform.scale(lair, (50, 50))
dungeon_ready = pg.transform.scale(dungeon, (50, 50))
party_ready = pg.transform.scale(party, (50, 50))
loadLists()

font = pg.font.SysFont('comic_sans', 25)
#Sprite Groups go here
markerGroup = pg.sprite.Group()
#Classes go here
        
class Hex():
    def __init__(self, surface, color, outline_color, radius, position, width=0):
        self.surface = surface
        self.color = color
        self.outline_color = outline_color
        self.radius = radius
        self.position = position
        self.width = width # Width of outline
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
class Faction():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos #The hex where the faction headquarters
        #Go ahead and render the faction name
        self.nameReady = font.render(name, True, WHITE)
#Class for party marker
class Marker(pg.sprite.Sprite):
    def __init__(self, surface, Hex, image, name, group, faction=None):
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
        self.faction = faction
    def setPosition(self, x, y):
        self.rect.center = (x, y)
    def setHex(self, Hex):
        self.Hex = Hex
        self.rect.center = self.Hex.position
    def getHex(self):
        return self.Hex
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        #If the mouse is hovering over the marker, display its name
        screen.blit(self.nameImage, self.rect.center)
        #If the marker is a part of a faction, display its name
        if self.faction:
            screen.blit(self.faction.nameReady, self.rect.midtop)
class Settlement(Marker): #You can spend gold to generate a new dungeon
    def __init__(self, surface, Hex, image, name, group, faction=False):
        super().__init__(surface, Hex, image, name, group, faction)
    def generateNewDungeon(self, gold, Hexes):
        #Attempt to take away one gold point, then generate random dungeon on the map.
        #Returns the generated marker
        newHex = Hexes[0]
        while newHex.token:
            newHex = random.choice(Hexes)
        return Dungeon(self.surface, newHex, dungeon_ready, "New Dungeon", self.group)
class Lair(Marker):
    def __init__(self, surface, Hex, image, name, group, faction=False):
        super().__init__(surface, Hex, image, name, group, faction)
class Dungeon(Marker):
    def __init__(self, surface, Hex, image, name, group, faction=False):
        super().__init__(surface, Hex, image, name, group, faction)

#UI for party members and HUD
class PartyUI(pg.sprite.Sprite):
    def __init__(self, group, surface, image, pos, partyList, rations, max_rations, gold, torches, max_torches, hirelings, max_hirelings):
        pg.sprite.Sprite.__init__(self, group)
        self.surface = surface
        self.partyList = partyList
        self.image = pg.transform.scale(image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        group.append(self)
        self.rations = rations
        self.max_rations = max_rations
        self.gold = gold
        self.torches = torches
        self.max_torches = max_torches
        self.hirelings = hirelings
        self.max_hirelings = max_hirelings
    def renderText(self, screen):
        text = ["Party: "]
        textarr = []
        for character in self.partyList:
            text.append(character.name + " " + character.descriptor + " " + str(character.level))
        for t in text:
            textarr.append(font.render(t, True, WHITE))
        return textarr
    def draw(self, screen):
        ration_text = font.render('Rations: ' + str(self.rations) + '/' + str(self.max_rations), True, WHITE)
        pos = (10, 10)
        screen.blit(ration_text, pos)
        ration_text = font.render('Torches: ' + str(self.torches) + '/' + str(self.max_torches), True, WHITE)
        pos = (10, 50)
        screen.blit(ration_text, pos)
        ration_text = font.render('Hirelings: ' + str(self.hirelings) + '/' + str(self.max_hirelings), True, WHITE)
        pos = (10, 90)
        screen.blit(ration_text, pos)
        gold_text = font.render('Gold: ' + str(self.gold), True, WHITE)
        pos = (10, 130)
        screen.blit(gold_text, pos)
        text = self.renderText(screen)
        screen.blit(self.image, self.rect.topleft)
        for i, t in enumerate(text):
            screen.blit(t, (self.rect.left, self.rect.top + (i * 50)))
#Do setup stuff here
simulation = True
Hexes = []
width = 50
start = (width, width)
imax=12
jmax=8
#Make the hex map
colors = [mountain_color, hill_color, forest_color, grass_color, beach_color, water_color]
for j in range(jmax):
    for i in range(imax):
        Hexes.append(Hex(screen, colors[-1], BLACK, width, (start[0]+(i*width*1.5), start[1]+(width*(i % 2))+(j*width*17/10)), 1))
def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n
def grabNearbyHexes(iHex):
    #Given a position of a hex, return all of the surrounding hexes
    toFind = []
    scan = -imax-1
    for j in range(2):
        for i in range(2):
            scan += 1
            if scan + iHex > 0 and scan + iHex < len(Hexes):
                toFind.append(scan+iHex)
        scan += imax
    return toFind
#Apply mountain algorithm
def runMountainsAlgorithm(Hex, iHex, iColor, change):
    #Takes a Hex and chooses each hex that is around them, then runs the algorithm each Hex.
    if not Hex.decided:
        Hex.decided = True
        newIColor = clamp(random.randint(iColor-change, iColor+change), 0, len(colors)-1)
        Hex.color = colors[newIColor]
        nextHexes = grabNearbyHexes(iHex)
        for h in nextHexes:
            runMountainsAlgorithm(Hexes[h], h, newIColor, change)
startingHexIndex = random.randint(0, len(Hexes)-1)
runMountainsAlgorithm(Hexes[startingHexIndex], startingHexIndex, 0, 1)

def generatePartyMember(): #Returns a PartyMember object
    memberName = random.choice(Names)
    memberClass = random.choice(Classes)
    memberLevel = 1
    memberType = random.choice(["m", "r", "s"])
    return PartyMember(memberName, memberLevel, memberClass, memberType)

#Create objects here
index = random.randint(0, len(Hexes)-2)
partyGroup = []
UIGroup = []
factions = []
for i in range(4):
    partyGroup.append(generatePartyMember())
party = Marker(screen, Hexes[index], party_ready, "party", markerGroup)

#Factions
locations = []
for i in range(4):
    location = None
    while not location or location in locations:
        if i == 0:
            location = Hexes[index+1]
        else:
            location = random.choice(Hexes)
    locations.append(location)
    name = random.choice(Adjectives).capitalize() + " " + random.choice(Animals).capitalize()
    factions.append(Faction(name, location))
    settlement = Settlement(screen, location, house_ready, random.choice(Adjectives).capitalize() + " " + random.choice(Settlements).capitalize(),
                            markerGroup, faction=factions[-1])

location = Hexes[index-1]
while location in locations:
    location = random.choice(Hexes)
locations.append(location)
starterDungeon = Dungeon(screen, location, dungeon_ready, "First Dungeon", markerGroup)


#Gameplay Variables
gold = 4
rations = 4
max_rations = 4
torches = 4
max_torches = 4
hirelings = 0
max_hirelings = 4
partyUI = PartyUI(UIGroup, screen, UIBackground, (620, 10), partyGroup, rations, max_rations, gold, torches, max_torches, hirelings, max_hirelings)
#Create TestMap
testMap = Map(screen, font, partyGroup, rations)
def generateEncounter(Table, Hex, factions):
    if not Hex.token:
        #Use the monster table to make an encounter
        encounter = monsters.generateItem()
        #50% chance to create / join a faction
        if random.randint(0, 1) == 0:
            newFaction = Faction(encounter["Name"], Hex)
            factions.append(newFaction)
        else:
            newFaction = factions[-1]
        return Lair(screen, Hex, lair_ready, encounter["Name"], markerGroup, faction=newFaction)

def checkForEncounters():
    percent = 10
    if random.randint(1, 100) < percent:
        generateEncounter(monsters, party.getHex(), factions)
def checkBoundaries(index, change, length):
    return (index+change) >= 0 and (index+change) < length
def move(change, index):
    party.setHex(Hexes[index+change])
    index += change
    if DepleteRations:
        if partyUI.rations > 0:
            partyUI.rations -= 1
        else:
            del partyGroup[0]
    checkForEncounters()
    return index
#Setup tables
monsters = tb(MonsterList)
running = True
DepleteRations = True
states = ["hexplore", "laircrawling", "dungeoncrawling"]
state = states[0]
currentMap = testMap

#Game Loop
while running:
    #Display
    screen.fill(background_color)
    #If at any point the partyGroup is empty, quit the game
    if not partyGroup:
        running = False
    if state == states[0]:
        for Hex in Hexes:
            Hex.draw()
        for marker in markerGroup:
            marker.draw(screen)
        #UI / HUD Section
        if simulation:
            for UIElement in UIGroup:
                UIElement.draw(screen)
        #All drawing needs to be done before this point.
        pg.display.flip()

        #Handle inputs
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r and partyUI.gold >= 1:
                        if isinstance(party.getHex().token, Settlement):
                                partyUI.gold -= 1
                                partyUI.rations = partyUI.max_rations
                                partyUI.torches = partyUI.max_torches
                    if event.key == pg.K_h and partyUI.gold >= 1:
                        if partyUI.hirelings+1 <= partyUI.max_hirelings:
                            partyUI.gold -= 1
                            partyUI.hirelings += 1
                            partyUI.max_rations += 1
                            partyUI.max_torches += 1
                        elif len(partyGroup) < 4:
                            partyUI.gold -= 1
                            partyGroup.append(generatePartyMember())
                    if event.key == pg.K_g:
                        if isinstance(party.getHex().token, Settlement) and partyUI.gold >= 1:
                            partyUI.gold -= 1
                            markerGroup.add(party.getHex().token.generateNewDungeon(partyUI.gold, Hexes))
                        elif isinstance(party.getHex().token, Dungeon) and partyUI.torches > 0:
                            state = states[1]
                            partyUI.torches -= 1
                        elif isinstance(party.getHex().token, Lair):
                            state = states[1]
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                #first make sure that the pos is in range of the original marker
                if math.hypot(party.rect.center[0] - pos[0], party.rect.center[1] - pos[1]) < (2*Hexes[0].radius):
                    #Then grab the Hex in range of the mouse and move the marker to the hex
                    for Hex in Hexes:
                        dist = math.hypot(Hex.position[0] - pos[0], Hex.position[1] - pos[1])
                        if dist < Hex.radius:
                            party.setHex(Hex)
                            if DepleteRations:
                                partyUI.rations -= 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    change = -imax
                    if checkBoundaries(index, change, len(Hexes)):
                       index = move(change, index)
                if event.key == pg.K_s:
                    change = imax
                    if checkBoundaries(index, change, len(Hexes)):
                        index = move(change, index)
                if event.key == pg.K_a:
                    change = -1
                    if checkBoundaries(index, change, len(Hexes)):
                        index = move(change, index)
                if event.key == pg.K_d:
                    change = 1
                    if checkBoundaries(index, change, len(Hexes)):
                        index = move(change, index)
            if event.type == pg.QUIT:
                running = False
    elif state == states[1]:
        screen.fill((0, 0, 0))
        currentMap.draw()
        pg.display.flip()
        if not currentMap.monsterPresent:
            #If there is no monster, grab which one should be present
            #Get monster from either the Lair name or a random one (if dungeon)
            if isinstance(party.getHex().token, Lair):
                monster = monsters.getItem("Name", party.getHex().token.name)
            else:
                monster = monsters.generateItem()
            currentMap.setMonster(monster)
        
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    #C to confirm running combat
                    currentMap.runCombat()
                if event.key == pg.K_r:
                    state = states[0]
                    currentMap.clearMonster()
            if event.type == pg.QUIT:
                running = False
        #If the currentMap is all updated (no new info is on the screen)
        #Return back to map
        if currentMap.get_ready():
            state = states[0]
            #reward gold for monsters defeated and level party members up
            partyUI.gold += (monster["Level"] * monster["Numbers"])
            for member in partyUI.partyList:
                if monster["Level"] >= member.level:
                    member.level += 1
            
pg.quit()


