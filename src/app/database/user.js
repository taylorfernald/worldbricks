const mongoose = require('mongoose');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

const characterSchema = new mongoose.Schema({
  name : {type: String},
  className : {type: String},
  level: {type: Number, 'default' : 1},
  hp: {type: Number, 'default': 1},
  maxhp: {type: Number, 'default': 1},
  body: {type: Number, 'default': 1},
  mind: {type: Number, 'default': 1},
  spirit : {type: Number, 'default': 1},
  //Lockdown doesn't need to be required here, just the id of the object we are looking for
  //If there is no lockdown, the string would be null.
  lockdown: {type: String},
  abilities: [String],
  magicItems: [String],
  notes: {type: String}
});

const userSchema = new mongoose.Schema({
  email: {                                
    type: String,                        
    required: true                        
  },
  name: {                                 
    type: String,                         
    required: true                        
  },
  characters: [characterSchema],                          
});

userSchema.methods.setPassword = function (password) {
    this.salt = crypto.randomBytes(16).toString('hex');
    this.hash = crypto
        .pbkdf2Sync(password, this.salt, 1000, 64, 'sha512')
        .toString('hex');
};

userSchema.methods.validPassword = function (password) {
  const hash = crypto
    .pbkdf2Sync(password, this.salt, 1000, 64, 'sha512')
    .toString('hex');                                      
  return this.hash === hash;                               
};

userSchema.methods.generateJwt = function () {
    const expiry = new Date();
    expiry.setDate(expiry.getDate() + 7);                
    return jwt.sign({                                    
        _id: this._id,                                     
        email: this.email,                                 
        name: this.name,                                   
        exp: parseInt(expiry.getTime() / 1000, 10),       
    }, process.env.JWT_SECRET );                                 
};

mongoose.model('User', userSchema);