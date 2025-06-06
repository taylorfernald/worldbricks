const mongoose = require('mongoose');
const dbURL = 'mongodb://localhost:27017/Worldbricks/';  
//const dbURL = 'mongodb+srv://cpsproductions7:SVEcZ1kQ1MSHUiqg@cluster0.qo04e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';

//Export the connect function so it actually runs
const connect = () => {
  setTimeout(() => mongoose.connect(dbURL, { useNewUrlParser: true, dbName: 'Worldbricks' }), 1000);
}      

//set debugging
mongoose.set('debug', true);

mongoose.connection.on('connected', () => {              
  console.log(`Mongoose connected to ${dbURL}`);         
});                                                      
mongoose.connection.on('error', err => {                 
  console.log(`Mongoose connection error: ${err}`);      
});                                                      
mongoose.connection.on('disconnected', () => {           
  console.log('Mongoose disconnected');                  
});                                                      
const gracefulShutdown = (msg, callback) => {            
  mongoose.connection.close(
    /*
    () => {                     
    console.log(`Mongoose disconnected through ${msg}`); 
    callback();}
    */
  );                                                    
};                                                       
// For nodemon restarts                                  
process.once('SIGUSR2', () => {                          
  gracefulShutdown('nodemon restart', () => {            
    process.kill(process.pid, 'SIGUSR2');                
  });                                                    
});                                                      
// For app termination                                   
process.on('SIGINT', () => {                             
  gracefulShutdown('app termination', () => {            
    process.exit(0);                                     
  });                                                    
});                                                      
// For Heroku / Render app termination                            
process.on('SIGTERM', () => {                            
  gracefulShutdown('Heroku app shutdown', () => {        
    process.exit(0);                                     
  });                                                    
});   

//Require the schemas
require('./user');
exports.connect = connect;