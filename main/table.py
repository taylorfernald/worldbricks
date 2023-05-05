import random
class Table():
    def __init__(self, List): #List of items to pull from
        self.List = List
    def generateItem(self): #Return a random item from the list
        return random.choice(self.List)
    def getItem(self, key, value): #Return a dict with the key/value combination
        for i in self.List:
            if i.get(key, None) == value:
                return i
        return None
