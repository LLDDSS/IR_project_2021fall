const express = require("express");

const PORT = 3001;

const app = express();
app.use(express.json());
var cors = require("cors");
app.use(cors());

let {PythonShell} = require('python-shell')
var options = {
    mode: 'text',
    scriptPath: './search_algorithm/',
    args: []
};


// Get search keywords from the frontend with POST method
app.post('/query', (req, res, next) => {
    const {terms} = req.body;
    let response;

    // Run search algorithm 
    options.args = [terms];
    PythonShell.run('main_search.py', options, function (err, results) {
        if (err) throw err;

        // Save output results into response
        response = results;

        // Convert response into json formate and pass it to the backend
        res.json({message: "Success!", data: response});
        });
});

app.post('/exact-search', (req, res, next)=>{
  const {terms} = req.body;
  let response;

  options.args = [terms]
  PythonShell.run('exact_search.py', options, function (err, results) {
      if (err) throw err;
      response = results;

      res.json({message: "Success!", data: response});
  });
});





app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});