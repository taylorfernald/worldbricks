#Has all of the data that belongs to a user held on the clientside. This means party and stronghold info
#Usually loaded from the server and initiatized with that info
import json


class User:
    def __init__(self, userinfo={}):
        #displayname, rations, max_rations, gold, torches, max_torches, hirelings, max_hirelings, partyList):
        #TODO: Change this so it accepts JSON / Dictionary and parses it.
        if userinfo:
            self.displayname = userinfo['name']
            self.userid = userinfo['_id']
            self.password = ""
            self.rations = userinfo['rations']
            self.max_rations = userinfo['max_rations'] 
            self.gold = userinfo['gold']
            self.torches = userinfo['torches']
            self.max_torches = userinfo['max_torches']
            self.hirelings = userinfo['hirelings']
            self.max_hirelings = userinfo['max_hirelings']
            self.partyList = userinfo['party']
            self.defaults = userinfo
            self.stronghold = None
        else:
            self.displayname = ""
            self.password = ""
            self.rations = 0
            self.max_rations = 0
            self.gold = 0
            self.torches = 0
            self.max_torches = 0
            self.hirelings = 0
            self.max_hirelings = 0
            self.partyList = []
            self.defaults = {}
            self.stronghold = None
    def getUI(self):
        ###Gets all the info needed to print to UI
        return [self.displayname, self.rations, self.max_rations, self.gold, self.torches, self.max_torches, self.hirelings, self.max_hirelings]
    def getParty(self):
        return self.partyList
    def tpk(self):
        ###Resets the user assuming they tpk (total party kill)
        #Only the stronghold and the account info survive
        #Everything else is reset to defaults
        self.rations, self.max_rations, self.gold, self.torches, self.max_torches, self.hirelings, self.max_hirelings, self.partyList = self.defaults
    def toJSON(self):
        ###Turns the current user object into a JSON form for sending to the server
        return json.dumps(
            self,
            default= lambda o : o.__dict__,
            sort_keys= True
        )