const express = require('express');
const app = express();
const port = 4000;
//Make CORS not an issue
app.use((req, res, next) => {
    res.header(`Access-Control-Allow-Origin",
        "http://localhost:${port}`);
    res.header("Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

//Handle Requests forwarded from Angular
app.get('api/userkey/info', (req, res) => {
    res.json({message:
        "Info GET recieved"
    });
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
})