const mongoose = require('mongoose');

const hexSchema = new mongoose.Schema({
  color: [Number],
  index: Number
})

const markerSchema = new mongoose.Schema({
  index: Number,
  type: String,
  name: String,
  defender: String
})

const terrainSchema = new mongoose.Schema({
  hexes: [hexSchema],
  markers: [markerSchema]
})

const terrainModel = mongoose.model('Terrain', terrainSchema, 'Terrain');

exports.terrainModel = terrainModel;
exports.terrainSchema = terrainSchema;