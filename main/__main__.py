import pygame as pg
import math
import random
from table import Table as tb
from monsters import MonsterList
from monsters import DefenderList
from creatures import *
from explore import *
from words import *
from constants import *
from resources import *
from user import User
from game_map import *
from rest import *

pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("World Bricks")
background_color = SKY_BLUE
screen.fill(background_color)
UIBackground.set_alpha(128)
loadLists()
#Activates if there is a UI on the screen that needs to be interacted with. Usually for textboxes or alerts.
UI_active = False
#Sprite Groups go here
markerGroup = pg.sprite.Group()
#Camera goes here
class Camera():
    def __init__(self, index):
        #Which index to focus on
        self.index = index
    def getOffset(self):
        #Get the tuple position away from the origin (0, 0)
        return (0, 0)

#UI for party members and HUD
class PartyUI(pg.sprite.Sprite):
    def __init__(self, group, surface, image, pos, user):
        pg.sprite.Sprite.__init__(self, group)
        self.surface = surface
        self.user = user
        self.image = pg.transform.scale(image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        group.append(self)
    def renderText(self, screen):
        text = [self.user.displayname + "'s Party: "]
        textarr = []
        for character in self.user.partyList:
            text.append(character.name + " " + character.descriptor + " " + str(character.level))
        for t in text:
            textarr.append(font.render(t, True, WHITE))
        return textarr
    def draw(self, screen):
        ration_text = font.render('Rations: ' + str(self.user.rations) + '/' + str(self.user.max_rations), True, WHITE)
        pos = (10, 10)
        screen.blit(ration_text, pos)
        ration_text = font.render('Torches: ' + str(self.user.torches) + '/' + str(self.user.max_torches), True, WHITE)
        pos = (10, 50)
        screen.blit(ration_text, pos)
        ration_text = font.render('Hirelings: ' + str(self.user.hirelings) + '/' + str(self.user.max_hirelings), True, WHITE)
        pos = (10, 90)
        screen.blit(ration_text, pos)
        gold_text = font.render('Gold: ' + str(self.user.gold), True, WHITE)
        pos = (10, 130)
        screen.blit(gold_text, pos)
        text = self.renderText(screen)
        screen.blit(self.image, self.rect.topleft)
        for i, t in enumerate(text):
            screen.blit(t, (self.rect.left, self.rect.top + (i * 50)))
#Do setup stuff here
rest = RestClient(server_url)
simulation = True
width = TILE_WIDTH
start = TILE_SCALE
imax=MAP_SIZE[0]
jmax=MAP_SIZE[1]
index = random.randint(0, (MAP_SIZE[0] * MAP_SIZE[1]) - 1) #where the party is rn
camera = Camera(index)
world = WorldMap(imax, jmax, screen, camera)
Hexes = world.generate()
currentPage = 0

#Note, move this over to the server so it can just make a new map.
#For the client, it would need to ask for data (a 2d array) and build up the map

def generatePartyMember(): #Returns a PartyMember object
    memberName = random.choice(Names)
    memberClass = random.choice(Classes)
    memberLevel = 1
    memberType = random.choice(["m", "r", "s"])
    return PartyMember(memberName, memberLevel, memberClass, memberType)

#Create objects here
partyGroup = []
UIGroup = []
factions = []
for i in range(4):
    partyGroup.append(generatePartyMember())
#The party needs to be drawn seperately
party = Marker(screen, world.getHex(index), party, "party", markerGroup, camera)

#Strongholds
for i in range(4):
    world.placeStructure(Stronghold)

starterDungeon = world.placeStructure(Dungeon, setName="Starting Dungeon")

#Make a dummy User (don't initailize anything yet) and connect the partyUI to it
user = User()
partyUI = PartyUI(UIGroup, screen, UIBackground, (620, 10), user)
#Create TestMap
testMap = Map(screen, font, partyGroup, rations)

def checkForEncounters():
    percent = 10
    if random.randint(1, 100) < percent:
        Lair(screen, world.getHex(index), lair, world.generateEncounter(monsters, world.getHex(index)), markerGroup, camera)

def move(change, index):
    if world.checkBoundaries(index, change):
        party.setHex(world.getHex(index+change))
        index += change
        if DepleteRations:
            if user.rations > 0:
                user.rations -= 1
            else:
                del partyGroup[0]
        checkForEncounters()
        return index
#Setup tables
monsters = tb(MonsterList)
running = True
DepleteRations = True
mainState = MainStates['TITLE']
currentMap = testMap

#Game Loop
while running:
    #Display
    screen.fill(background_color)
    #If at any point the partyGroup is empty, quit the game
    if not partyGroup:
        running = False
    
    if mainState == MainStates.HEXCRAWL:
        world.draw()
        party.draw(screen)
        #UI / HUD Section
        if simulation:
            for UIElement in UIGroup:
                UIElement.draw(screen)
        #All drawing needs to be done before this point.
        pg.display.flip()

        #Handle inputs
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if UI_active:
                    #handle UI controls
                    pass
                else:
                    change = 0
                    if event.key == pg.K_t:
                        mainState = MainStates.TUTORIAL
                    elif event.key == pg.K_ESCAPE:
                        #Save and quit
                        running = False
                    elif event.key == pg.K_w:
                        change = -imax
                    elif event.key == pg.K_s:
                        change = imax
                    elif event.key == pg.K_a:
                        change = -1
                    elif event.key == pg.K_d:
                        change = 1
                    if change and world.checkBoundaries(index, change):
                        index = move(change, index)
                    if event.key == pg.K_RSHIFT and user.gold >= 1:
                        if isinstance(party.getHex().token, Stronghold):
                                user.gold -= 1
                                user.rations = user.max_rations
                                user.torches = user.max_torches
                    if event.key == pg.K_LSHIFT and user.gold >= 1:
                        if user.hirelings+1 <= user.max_hirelings:
                            user.gold -= 1
                            user.hirelings += 1
                            user.max_rations += 1
                            user.max_torches += 1
                        elif len(partyGroup) < 4:
                            user.gold -= 1
                            partyGroup.append(generatePartyMember())
                    if event.key == pg.K_RETURN:
                        #Strongholds count as a settlement for this player.
                        if isinstance(party.getHex().token, Settlement) and user.gold >= 1:
                            user.gold -= 1
                            world.generateEncounter(monsters, world.verifyRandomHex(), factions)
                        elif isinstance(party.getHex().token, Dungeon) and user.torches > 0:
                            mainState = MainStates.BATTLE
                            user.torches -= 1
                        elif isinstance(party.getHex().token, Lair) | isinstance(party.getHex().token, Stronghold):
                            mainState = MainStates.BATTLE
                        else:
                            #otherwise, assuming the player has enough money, they can build a settlement here.
                            #The defenses scale with how much money the stronghold has. 
                            if user.gold >= 1:
                                user.gold -= 1000
                                Stronghold(screen, party.getHex(), "Player", markerGroup, money=1000)
            if event.type == pg.QUIT:
                running = False

    elif mainState == MainStates.BATTLE:
        screen.fill((0, 0, 0))
        currentMap.draw()
        pg.display.flip()
        if not currentMap.monsterPresent:
            #If there is no monster, grab which one should be present
            #Get monster from either the Lair name or a random one (if dungeon)
            if isinstance(party.getHex().token, Lair):
                monster = monsters.getItem("Name", party.getHex().token.name)
            elif isinstance(party.getHex().token, Stronghold):
                #Builds a monster entry from the stronghold defender class
                s = party.getHex().token
                monster = s.defender
            else:
                monster = monsters.generateItem()
            currentMap.setMonster(monster)
        
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if UI_active:
                        pass #UI controls
                    else:
                        #Confirm running combat
                        currentMap.runCombat()
                if event.key == pg.K_RSHIFT:
                    if UI_active:
                        pass #UI controls
                    else:
                        mainState = MainStates.HEXCRAWL
                        currentMap.clearMonster()
            if event.type == pg.QUIT:
                running = False
        #If the currentMap is all updated (no new info is on the screen)
        #Return back to map
        if currentMap.get_ready():
            mainState = MainStates.HEXCRAWL
            #reward gold for monsters defeated and level party members up
            user.gold += (monster["Level"] * monster["Numbers"])
            #If they just took on a stronghold, give that money too.
            if isinstance(party.getHex().token, Stronghold):
                user.gold += party.getHex().token.stash
                party.getHex().token.stash = 0 
            for member in user.partyList:
                if monster["Level"] >= member.level:
                    member.level += 1
    elif mainState == MainStates.TUTORIAL:
        #Show the game "manual". Basically pages of text and images that the player can flip through
        screen.fill(BLACK)

        for index, line in enumerate(tutorial_pages[currentPage]):
            shownText = font.render(line, True, WHITE)
            screen.blit(shownText, (10, 30*index+10), None)

        pg.display.flip() #Draw before this point

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    currentPage += 1
                    if currentPage >= len(tutorial_pages): currentPage = 0
                if event.key == pg.K_a:
                    currentPage -= 1
                    if currentPage < 0: currentPage = len(tutorial_pages) - 1
                if event.key == pg.K_ESCAPE:
                    mainState = MainStates.HEXCRAWL
            if event.type == pg.QUIT:
                running = False
    elif mainState == MainStates.TITLE:

        title_text = font.render("World Bricks", False, WHITE)
        screen.blit(title_text, (width / 2, height / 2))

        input_text = font.render("Enter", False, WHITE)
        screen.blit(input_text, (width / 2, height / 2 + TILE_WIDTH))

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    mainState = MainStates.USERNAME
            if event.type == pg.QUIT:
                running = False
    elif mainState == MainStates.USERNAME or mainState == MainStates.PASSWORD:
        title_text = font.render("Sign in", False, WHITE)
        screen.blit(title_text, (width / 2, height / 2))

        enter_username_text = font.render("Enter username" if mainState == MainStates.USERNAME
                                     else "Enter password", False, WHITE) 
        
        screen.blit(enter_username_text, (width / 2, height / 2 + TILE_WIDTH))

        username_text = font.render(user.displayname if mainState == MainStates.USERNAME
                               else user.password, False, WHITE)
        screen.blit(username_text, (width / 2, height / 2 + (TILE_WIDTH * 2)))

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                #Make these work with the username / password respectively
                if event.key == pg.K_BACKSPACE:
                    if mainState == MainStates.USERNAME:
                        user.displayname = user.displayname[:-1]
                    else:
                        user.password = user.password[:-1]
                elif event.key == pg.K_RETURN:
                    mainState = MainStates.PASSWORD if mainState == MainStates.USERNAME else MainStates.LOADING
                else: 
                    if mainState == MainStates.USERNAME:
                        user.displayname += event.unicode
                    else:
                        user.password += event.unicode
            if event.type == pg.QUIT:
                running = False
    elif mainState == MainStates.LOADING:
        #TODO: Do authentication stuff and establish a connection here
        title_text = font.render("Loading...", False, WHITE)
        screen.blit(title_text, (width / 2, height / 2))

        pg.display.flip()

        rest.verify_user_key(user.displayname, user.password)

        #Setup the user object
        user = User(rest.get_user_info())
        print("User key is: " + rest.userkey)
        #For now, skip to the gameplay
        mainState = MainStates.HEXCRAWL

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
pg.quit()


