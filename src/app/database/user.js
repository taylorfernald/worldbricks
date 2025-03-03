const mongoose = require('mongoose');

const characterSchema = new mongoose.Schema({
  damagetype: {type: String, default: "m"},
  level: {type: Number, default: 1},
  name: {type: String, default: ""},
  occupation: {type: String, default: "Unknown"}
})

const strongholdSchema = new mongoose.Schema({
  defenderName: {type: String, default: "None"},
  positionX: {type: Number, default: 0},
  positionY: {type: Number, default: 0}
})

const userSchema = new mongoose.Schema({
  name: {                                 
    type: String,                         
    required: true,
    default: "Unnamed User"                        
  },
  gold : {type: Number, default: 0},
  hirelings : {type: Number, default: 0},
  party: [characterSchema],
  rations : {type: Number, default: 0},
  stronghold: strongholdSchema
});

const userModel = mongoose.model('User', userSchema, 'Users');

exports.userModel = userModel;