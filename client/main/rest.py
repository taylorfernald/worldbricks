#This class's job is to act as a client for the host. It sends REST requests on behalf of the game
import requests
import json

class RestClient():
    def __init__(self, server_url):
        self.url = server_url #Where is the server?
        self.userkey = "67c0a8171abe9aa514aadf4e"
        self.busy = False #Prevents DDOS attacks on our poor server
    def verify_user_key(self, username, password):
        #Send the calculated passkey to the server.
        #The server uses the username and password to check the passkey.
        #If the server returns with True, then the passkey is correct and can be used in the future.
        #THIS IS NOT SAFE, just a proof of concept for now.
        #This should be used in the initial authentication (log in for session) step. The userkey acts as the sessionid
        self.calculate_user_key(username, password)
        response = requests.get(self.url + f"/{self.userkey}")
        return response
    def calculate_user_key(self, username, password):
        #Make a passkey. This is simple just to get something to work. A more secure way would be needed later.
        self.userkey = username + password
    def get_user_info(self):
        if not self.busy:
            self.busy = True
            print("Sending request...")
            #Using the userkey, get the user info
            print(f"{self.url}/{self.userkey}/info")
            response = requests.get(self.url + f"{self.userkey}/info")
            response = response.json()
            print(response)
            return response
        return 0
    def get_world_info(self):
        response = requests.get(self.url + f"/{self.userkey}/getworld")
        #Gets the view of the world on behalf of the user
        return response
    def set_stronghold(self, position):
        #Adds a new stronghold to the world at a position. The server needs to verify this.
        response = requests.post(self.url + f"/{self.userkey}/stronghold/{position}")
        return response 
    def clear_stronghold(self, position):
        #The user destroyed the stronghold. Remove the money from it.
        response = requests.put(self.url + f"/{self.userkey}/stronghold/{position}")
        return response 
    def save_user_info(self, user):
        #Put the user's info on the server.
        #Note you do need to pass in the user here.
        print("Attempting a save to the server...")
        response = requests.put(self.url + f"{self.userkey}/save", json=user.toJSON())
        print(user.toJSON())
        if response:
            print("Save successful")
        else:
            print("There was a problem with contacting the server.")
        return response
