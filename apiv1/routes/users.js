var express = require('express');
var router = express.Router();
var Sql = require('../mysql.js')
var activity = require('../activity.js')
var md5 = require('md5')

/* GET users listing. */
router.post('/auth', function(req, res, next) {
  
  if (req.session.logged_in && req.session.logged_in == true) {
    return res.json(req.session.user);
  } else {

    var err_msg = 'invalid username or password';
    if (!req.body.username || !req.body.password) {
      return res.json({
        error: err_msg
      });
    }
    
    var params = [req.body.username, req.body.username, req.body.username, md5(req.body.password)]
    
    var handler = (err, result, fields) => {
      console.log(err)
      if (err || result.length < 1) return res.json({error: err_msg, e: err})
      req.session.user = result[0]
      req.session.logged_in = true
      res.json(result[0]);
    }
    Sql.query('select * from `user` where (email = ? or username = ? or phone = ? ) and `password` = ?', params, handler);
  }
  
});

router.post('/location', function (req, res, next) {
  var currentUser = req.session.user;
  if (!req.body.lat || !req.body.lon) {
    res.json({
      error: 'lat and lon options are required'
    })
  }

  var _query = 'INSERT INTO `user_locations` (lat, lon, user_id) values (?, ?, ?)';

  Sql.query(_query, [req.body.lat, req.body.lon, currentUser.id], (er, result, fields) => {
      if (er) 
          return res.json(er);
      return res.json({
        'location_id': result.insertId
      });

  });
});







module.exports = router;
