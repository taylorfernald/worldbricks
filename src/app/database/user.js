const mongoose = require('mongoose');
const terrainSchema = require('./terrain').terrainSchema;

const characterSchema = new mongoose.Schema({
  damagetype: {type: String, default: "m"},
  level: {type: Number, default: 1},
  name: {type: String, default: ""},
  occupation: {type: String, default: "Unknown"}
})

const userSchema = new mongoose.Schema({
  name: {                                 
    type: String,                         
    required: true,
    default: "Unnamed User"                        
  },
  position_index: {type: Number, default: 0},
  gold : {type: Number, default: 0},
  party: [characterSchema],
  rations : {type: Number, default: 4},
  max_rations : {type: Number, default: 4},
  terrain: {type: terrainSchema},
  torches : {type: Number, default: 4},
  max_torches : {type: Number, default: 4},
  hirelings : {type: Number, default: 0},
  max_hirelings: {type: Number, default: 4}
});

const userModel = mongoose.model('User', userSchema, 'Users');

exports.userModel = userModel;