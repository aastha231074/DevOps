var express = require('express');
var path = require('path');
var app = express();

// Serve static files from public directory
app.use(express.static('public'));

const URL = process.env.BACKEND_URL || 'http://localhost:8000/api';

const fetch = (...args) =>
    import('node-fetch').then(({ default: fetch }) => fetch(...args));

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/data', async function (req, res) {
    const options = {
        method: 'GET'
    };
    
    try {
        let response = await fetch(URL, options);
        const data = await response.json();
        res.json(data);
    } catch (err) {
        console.log('Backend fetch error:', err);
        res.status(500).json({ msg: `Internal Server Error: ${err.message}` });
    }
});

app.listen(3000, function () {
    console.log('Ares listening on port 3000!')
});