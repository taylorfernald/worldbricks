import requests, json, os

#Grab the file, get the JSON from it then send the request to the server at the correct ip
settings_path = "./settings.json"
running = True

def getModified(path):
    return os.path.getmtime(path)

def updateServer(settingsFile):
    trackerURL = settingsFile["trackerURL"]
    belongsTo = settingsFile["belongsTo"]
    parentComponent = settingsFile["parentComponent"]
    selfComponent = settingsFile["selfComponent"]
    port = settingsFile["port"]
    component = settingsFile["component"]
    name = settingsFile["name"]
    _id = settingsFile["_id"]

    print(f"Uploading to: {trackerURL + belongsTo}")
    try:
        response = requests.put(trackerURL + belongsTo, json={"_id" : _id, "name" : name, "parentip" : parentComponent, "ip" : selfComponent, "port" : port, "component" : component})

    except ConnectionRefusedError:
        print("Connection refused by server. Try a different URL")

    except Exception as error:
        print(f"Given error ${error}")

    finally:
        print(f"Completed updating attempt.")

def detectFileChangesLoop(path):
    print(f"Checking for changes on file path {path}.")
    lastModified = getModified(path)
    while running:
        detectFileChanges(lastModified, path)

def detectFileChanges(lastModified, path):
    currentModified = getModified(path)
    if lastModified != currentModified:
        lastModified = currentModified
        settingsFile = open(path)
        settingsFile = json.load(settingsFile)
        updateServer(settingsFile)


detectFileChangesLoop(settings_path)
    

