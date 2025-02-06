require('dotenv').config();
const app = require('./app');
const ViteExpress = require("vite-express");

const {PORT} = process.env;

ViteExpress.listen(app, PORT, () =>
  console.log("Server is listening at http://localhost:" + PORT)
);

// const express = require('express');
// const app = express();
// const apiRouter = require('./api');

// // Middleware to parse JSON in request bodies
// app.use(express.json());

// // API Routes (should come before static file serving)
// app.use('/api', apiRouter); 

// // Serve static files (React frontend)
// app.use(express.static(path.join(__dirname, 'public')));

// // Catch-all for any route not matched by above (optional but recommended for React routing)
// app.get('*', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'index.html'));
// });
