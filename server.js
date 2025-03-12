const express = require('express');
const { usersReadOne, usersUpdateOne } = require('./src/app/database/data-controller');
const app = express();
const port = 4000;
//dev: http://localhost:8080
//prod: https://worldbricks-906949648363.us-east1.run.app/

//Make CORS not an issue
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", 
               "http://localhost:8080");
    res.header("Access-Control-Allow-Headers", 
               "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

//Handle Requests forwarded from Angular

//Sanity check
app.get('/api/', (req, res) => {
    res.json({message: 
        "Base API works"
    })
})

app.get('/api/:userid/info', usersReadOne);

app.get('/api/userkey/getworld', (req, res) => {
    res.json({message:
        "Info GET recieved"
    });
});

app.post('/api/userkey/stronghold/position', (req, res) => {
    res.json({message:
        "Info POST recieved"
    });
});

app.put('/api/userkey/stronghold/position', (req, res) => {
    res.json({message:
        "Info PUT recieved"
    });
});

app.put('/api/:userid/save', usersUpdateOne);

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
})