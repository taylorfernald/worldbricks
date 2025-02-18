import sys
#List of words / phrases sorted by category
Animals = []
Settlements = []
Adjectives = []
Actions = []
Colors = []
Names = []
Classes = []

def loadLists():
    path = "main/words.txt"
    file = open(path, "r")
    #Animals
    for i in range(int(file.readline())):
        Animals.append(file.readline()[:-1])
    #Settlements
    for i in range(int(file.readline())):
        Settlements.append(file.readline()[:-1])
    #Adjectives
    for i in range(int(file.readline())):
        Adjectives.append(file.readline()[:-1])
    #Actions
    for i in range(int(file.readline())):
        Actions.append(file.readline()[:-1])
    #Colors
    for i in range(int(file.readline())):
        Colors.append(file.readline()[:-1])
    #Names
    for i in range(int(file.readline())):
        Names.append(file.readline()[:-1])
    #Classes
    for i in range(int(file.readline())):
        Classes.append(file.readline()[:-1])
