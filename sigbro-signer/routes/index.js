var express = require('express');
var router = express.Router();

let access_token = process.env.ACCESS_TOKEN || ''; 

/* GET home page. */
router.get('/', function(req, res, next) {
  res.sendStatus(404);
  // res.render('index', { title: 'Sigbro Hackathon' });
});

/* GET health check. */
router.get('/ping', function(req, res, next) {
  if ( access_token.length < 10 ) {
    res.sendStatus(503); 
  } else { 
    res.json({ping: 'pong'});
  }
});


module.exports = router;
