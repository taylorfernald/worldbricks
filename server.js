const express = require('express');
const app = express();
const port = 4000;

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

app.get('/api/userkey/info', (req, res) => {
    res.json({message:
        "Info GET recieved"
    });
});

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

app.put('/api/userkey/save', (req, res) => {
    res.json({message:
        "Info PUT recieved"
    });
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
})