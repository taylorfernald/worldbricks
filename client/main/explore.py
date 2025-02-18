import pygame as pg
import random
from words import *
from resources import *

class TransferRooms():
    def __init__(self):
        pass
class Combat():
    def __init__(self, partyList):
        self.partyList = partyList
        self.monster = None
    def runCombat(self): #Should receive this signal from generateEncounters when the fight should start.
        #setup a list of things to have the info box say
        text = []
        #Making sure we have all of the info we need:
        #Set up the monster's data structures
        self.defences = self.monster['CC']
        #x is shield, v is heart, f is flight, o is mist.
        self.types = self.monster['Types'][::-1]
        #r is ranged, m is melee, s is spell
        self.hp = self.monster['Level']
        self.number = self.monster['Numbers']

        text.append(self.monster["Name"] + " approaches!")
        
        #Do this until either party is completely gone
        inBattle = True
        while inBattle:
            hit = False
            #resolve the party round
            for member in self.partyList:
                if self.checkHit(member.attackingtype, self.defences[-1]):
                    hit = True
                    self.hp -= member.level
                    if len(self.defences) > 1:
                        self.defences = self.defences[:-1]
                        text.append("Removed one tag.")
                    text.append(member.name + " hits for " + str(member.level))
                    if self.hp <= 0:
                        self.number -= 1
                        text.append("This kills " + self.monster["Name"] + "!")
                        if self.number <= 0:
                            inBattle = False
                            text.append("No more targets left!")
                            break
                else:
                    text.append(member.name + " misses (wrong damage type)!")
                    
            #resolve the monster round
            for i in range(self.number):
                if self.checkHit(self.types, self.partyList[0].attackingtype):
                    hit = True
                    self.partyList[0].level -= self.monster['Level']
                    text.append(self.monster['Name'] + " " + random.choice(Actions) + " the party for " + str(self.monster['Level']) + "!")
                    if self.partyList[0].level <= 0:
                        text.append("It kills " + self.partyList[0].name + "!")
                        del self.partyList[0]
                else:
                    text.append(self.monster["Name"] + " misses (wrong damage type)!")
            if not hit: #Noone has been able to hit each other
                text.append("No one can hit each other!")
                #Kill all but one party member, but award the win
                while len(self.partyList) > 1:
                    del self.partyList[0]
                break;
        text.append("Terminated")
        text.append("!")
        return text
    def checkHit(self, attacker, defender):
        #Takes in the string tags and returns a boolean value
        #Checks if the attack can hit.
        #Hearts are automatically a hit.
        #Flying creatures can only be hit by ranged.
        #Shielded creatures can only be hit by melee.
        #Misted creatures can only be hit by spells.
        #Otherwise, the tags need to match.
        if defender == 'v':
            return True
        elif defender == attacker:
            return True
        elif defender == 'x' and attacker == 'm':
            return True
        elif defender == 'f' and attacker == 'r':
            return True
        elif defender == 'o' and attacker == 's':
            return True
        else:
            return False
class GenerateEncounters():
    def __init__(self, partyList):
        self.c = Combat(partyList)
        self.monster = None
    def runCombat(self):
        return self.c.runCombat()
    def setMonster(self, monster):
        self.monster = monster
        self.c.monster = monster
class Info():
    def __init__(self, screen, font, color):
        self.screen = screen
        self.font = font
        self.color = color
        self.arr = [""]
        self.index = 0
        #Probably a bad idea to put this only here, but oh well...
        self.clock = pg.time.Clock()
        self.timer = 0
        self.timeLimit = 1000
    def update(self):
        if self.arr[0] != "":
            self.clock.tick(60)
            self.timer += self.clock.get_time()
            if self.timer >= self.timeLimit:
                self.timer = 0
                self.index += 1
                if self.index >= len(self.arr):
                    self.index = 0
                    self.arr = [""]
    def draw(self):
        self.update()
        text = self.font.render(self.arr[self.index], True, self.color)
        self.screen.blit(text, (self.screen.get_width()/3, self.screen.get_height()/4*3))
    def get_ready(self):
        return self.arr[self.index] == "!"
class Party():
    def __init__(self, screen, font, color, partyList):
        self.screen = screen
        self.font = font
        self.partyList = partyList
        self.color = color
    def draw(self):
        for i, character in enumerate(self.partyList):
            text = self.font.render(character.name + " " + str(character.level), True, self.color)
            self.screen.blit(text, (self.screen.get_width()/4*3, self.screen.get_height()/3+(text.get_height() * i)))
            #Draw the attacking type seperately
            if character.attackingtype == "m": attacking_sprite = melee
            elif character.attackingtype == "r": attacking_sprite = ranged
            else: attacking_sprite = magic

            self.screen.blit(attacking_sprite, (self.screen.get_width()/4*3 - 20, self.screen.get_height()/3+(text.get_height() * i)))
class Monster():
    def __init__(self, screen, font, color):
        self.screen = screen
        self.font = font
        self.color = color
        self.monster = None #The database entry for the monster
        self.number = 0
    def set_monster(self, monster):
        self.monster = monster
    def draw(self):
        if self.monster:
            text = self.font.render(str(self.monster["Numbers"]) + " x " + self.monster["Name"] + " L" + str(self.monster["Level"]), True, self.color)
            self.screen.blit(text, (self.screen.get_width()/4, self.screen.get_height()/2))
            #TODO: put the attacking symbol in the right place
            tags = self.font.render(self.monster["Types"] + " : " + str(self.monster["CC"]), True, self.color)
            #Print the icons
            self.screen.blit(letter_to_tag[self.monster["Types"]], (self.screen.get_width()/4, self.screen.get_height()/2+40))
            for i, letter in enumerate(self.monster["CC"]):
                self.screen.blit(letter_to_tag[letter], (self.screen.get_width()/4 + (i*ICON_SIZE[0]), self.screen.get_height()/2+54))
class UI():
    def __init__(self, screen, font, partyList, monster, torches):
        self.partyList = partyList
        self.torches = torches
        self.font = font
        self.screen = screen
        self.color = (255, 255, 255)
        #Child classes
        self.info = Info(self.screen, self.font, self.color)
        self.party = Party(self.screen, self.font, self.color, self.partyList)
        self.monster = Monster(self.screen, self.font, self.color)
        self.monster.set_monster(monster)
    def setText(self, text):
        self.info.arr = text
        self.info.timer = 0
    def draw(self):
        text = self.font.render("", True, self.color)
        self.screen.blit(text, (10, 10))
        self.party.draw()
        self.info.draw()
        self.monster.draw()
    def get_ready(self):
        return self.info.get_ready()
class Map():
    def __init__(self, Surface, font, partyList, torches):
        #Child classes that have jobs
        self.ge = GenerateEncounters(partyList)
        self.ui = UI(Surface, font, partyList, self.ge.monster, torches)
        self.tr = TransferRooms()
        self.monsterPresent = False
    def runCombat(self):
        text = self.ge.runCombat()
        self.ui.setText(text)
    def setMonster(self, monster):
        self.monsterPresent = True
        self.ge.setMonster(monster)
        self.ui.monster.set_monster(monster)
    def clearMonster(self):
        self.monsterPresent = False
    def draw(self):
        self.ui.draw()
    def get_ready(self):
        #Returns whether the map is ready to switch back
        ret = self.ui.get_ready()
        if ret:
            self.monsterPresent = False
        return ret
