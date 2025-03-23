const express = require('express');
const app = express();
const port = 3000;

// Serve static files
app.use(express.static(__dirname));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/map.html');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
