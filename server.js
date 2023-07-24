const express = require('express');
const app = express();
const host = "http://localhost"
const port = 8081

// We'll use the dist directory to serve the Vue App
app.use(express.static('dist'));

app.listen(port, () => {
 console.log(`App listening on ${host}:${port}`);
});
