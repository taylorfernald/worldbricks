class Creature():
    def __init__(self, name, level, descriptor, attackingtype):
        self.name = name
        self.level = level
        self.descriptor = descriptor
        self.attackingtype = attackingtype
class PartyMember(Creature):
    def __init__(self, name, level, descriptor, attackingtype):
        super().__init__(name, level, descriptor, attackingtype)
    
