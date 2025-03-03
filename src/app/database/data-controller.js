const mongoose = require('mongoose');
const users = require('./user').userModel;
const db_connect = require('./db').connect;

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
const usersReadOne = (req, res) => {
    users
      .findById(req.params.userid)
      .then((user) => {
        console.log(`::${user}`);
        return res
            .status(200)
            .json(user);
      })
      .catch((err) => {
        console.log(`There was an error: ${err}`);
        return res
            .status(404)
            .json(err)
      })
};
const usersUpdateOne = (req, res) => {
  if (!req.params.userid) {
    return res
      .status(404)
      .json({
        "message": "Not found, userid is required"
      });
  }
  users
    .findById(req.params.userid)                          
    .exec((err, user) => {
      if (!user) {
        return res
          .json(404)
          .status({
            "message": "userid not found"
          });
      } else if (err) {
        return res
          .status(400)
          .json(err);
      }
      user.name = req.body.name;                            
      user.email = req.body.email;                                                                               
      user.save((err, u) => {                            
        if (err) {
          res                                                   
            .status(404)
            .json(err);
        } else {
          res                                                   
            .status(200)
            .json(u);
        }
      });
    }
  );
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