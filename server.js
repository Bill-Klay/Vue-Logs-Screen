const express = require('express');
const path = require('path');
const app = express();
const host = "http://localhost"
const port = 8081

// We'll use the dist directory to serve the Vue App
app.use(express.static('dist'));

// All other GET requests not handled before will return our Vue app
app.get('*', (req, res) => {
 res.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
 console.log(`App listening on ${host}:${port}`);
});
