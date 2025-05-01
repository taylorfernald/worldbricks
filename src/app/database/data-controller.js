const mongoose = require('mongoose');
const users = require('./user').userModel;
const terrain = require('./terrain').terrainModel;
const db_connect = require('./db').connect;
const fs = require('node:fs');
const terrainId = "67d478eb115486e92b338b30"

db_connect();

const usersCreate = (req, res) => {
  users.create({
    name : req.body.name
  }, (err, user) => {
    if (err) {
      res
        .status(400)
        .json(err);
    } else {
      res
        .status(201)
        .json(user);
    }
  })
};
const usersReadOne = async (req, res) => {
    const terrainToSend = await terrain.findById(terrainId);
    users
      .findById(req.params.userid)
      .then((user) => {
        userToSend = {
          _id: user._id,
          name: user.name,
          position_index : user.position_index,
          gold: user.gold,
          party: user.party,
          rations: user.rations,
          max_rations: user.max_rations,
          torches: user.torches,
          max_torches: user.max_torches,
          hirelings: user.hirelings,
          max_hirelings: user.max_hirelings,
          terrain: terrainToSend
        }
        console.log(`:: ${userToSend}`);
        return res
            .status(200)
            .json(userToSend);
      })
      .catch((err) => {
        console.log(`There was an error: ${err}`);
        return res
            .status(404)
            .json(err)
      })
};

//Used for saving
const usersUpdateOne = (req, res) => {
  if (!req.params.userid) {
    return res
      .status(404)
      .json({
        "message": "Not found, userid is required"
      });
  }

  file = fs.createWriteStream('./req.txt');
  req.pipe(file); //This reads the body to a text file correctly
  console.log("Saving server side.");

  const chunks = [];
  content = "";

  req.on('readable', () => {
    let chunk;
    while (null !== (chunk = req.read())) {
      chunks.push(chunk);
    }
  });

  req.on('end', () => {
    content = JSON.parse(chunks.join('').replace(/\\/g, '').slice(1, -1));
  });
  
  users
    .findById(req.params.userid)
    .then((user) => {
      user.gold = content.gold;
      user.hirelings = content.hirelings;
      user.party = content.partyList;
      user.rations = content.rations;
      user.stronghold = content.stronghold;
      user.max_hirelings = content.max_hirelings;
      user.max_rations = content.max_rations;
      user.max_torches = content.max_torches;
      user.position_index = content.position_index;

      //TODO: Change this to update the terrain collection.
      if ("terrain" in content) {
        // TODO: Compare this with the strongholds we already have and update any
        terrain.findById(terrainId)
        .then((storedTerrain) => {
            storedTerrain.markers = content.terrain.markers;
            storedTerrain.save();
          }
        )
      }

      user.save();
      console.log("Saving complete on the server side");
      return res.status(200).json({"message": `Good to go for ${user._id}`});})
    .catch((err) => {
      console.log(`Error: ${err}`);
      return res.status(400).json(err);})
};
const usersDeleteOne = (req, res) => {
  const {userid} = req.params;
  if (userid) {
    users
      .findByIdAndRemove(userid)          
      .exec((err, user) =>  {             
          if (err) {
            return res                        
              .status(404)
              .json(err);
          }
          res                                 
            .status(204)
            .json(null);
        }
    );
  } else {
    res
      .status(404)
      .json({
        "message": "No User"
      });
  }
};

module.exports = {
    usersCreate,
    usersReadOne,
    usersUpdateOne,
    usersDeleteOne
}