<h1>Installation Instructions</h1>

This section has two parts. The first describes how to install it client side and the second
describes how to install it on the node.js server

<h2> Part 1. Server Side </h2>
To create a new server, add a new document to a mongoDB server whose document matches the following (you do need to create it with at least one component):
{
  "_id": {
    "$oid": "EXAMPLE_ID"
  },
  "name": "ExampleIOT",
  "components": [
    {
      "_id": {
        "$oid": "SEPERATE_ID"
      },
      "name": "Server",
      "ip": "192.168.0.5",
      "port": 800
    }
  ]
}

Then add your created Id for the IoT as the <b>belongsTo</b> field in settings.json.
Finally, run the website using npm start in a terminal.

<h2> Part 1. Client Side </h2>
The following needs to be done for EACH component in your IoT (even servers / controllers).
<ol>
<li> Replace the information in settings.json with your component's settings. </li>
<li> Either run the IOTUpdater python file or run its detectFileChanges function for each component. This uploads the information from the settings file to the server for its component </li>
</ol>

<h1>Operation Instructions (How to use the Website)</h1>

When you first startup the website, you should see a box named "Loading" on the screen.
If the box matches your IoT, you may skip this paragraph. In the top box, type in the id for the IoT you wish to view and press the button near it. This should load the IoT by that id and display it on the screen.

To shut down the server, in the terminal where the server is running, use Ctrl-C (like you are copying text).

<h2> Troubleshooting </h2>

This section has common problems and several common reasons why they would happen.
To help troubleshoot, follow each step in order until your issue is resolved.

Problem: I can't see my IoT on the screen.
Steps: 
<ol>
<li>Check if your Mongo database is connected using either the command line or Compass.</li>
<li>Check if you are connected to the server on the correct port. The website should say the correct port in the terminal when it first starts up. 
<li>Check to make sure that there are no errors in the terminal.</li>
<li>Look at compass to make sure that your id is correct and that the document matches the above specification.</li>
</ol>
