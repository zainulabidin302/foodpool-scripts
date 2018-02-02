var debug = require('debug')('apiv1:server');
var express = require('express');
var router = express.Router();

var Sql = require('../mysql.js')


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/query', function(req, res, next) {
    if (!req.body.query) {
        return res.json({error: 'query not found'})
    }
    
    Sql.query(req.body.query, (er, result, fields) => {
        if (er) {
            return res.json({
                error: er,
                'result': result,
                fields: fields
            })
        }
        return res.json({
                'result': result,
                fields: fields
        });
    });
    
})




router.get('/feed/location/:lat/:lon/:radius?', function(req, res, next) {
  
  if (!req.params.lat || !req.params.lat)
  return res.json({
      error: 'location is missing'
  })
  let radius = req.params.radius || 1;
  let lat = req.params.lat;
  let lon = req.params.lon;
  
  let user = req.body.user;
  
  let query = 'SELECT * ,' +
                `( 6371 * acos( cos( radians(${lat}) ) * cos( radians( lat ) ) * cos( radians( lon ) -` +
                `radians(${lon}) ) + sin( radians(${lat}) ) * sin( radians(lat) ) ) ) AS distance` +
                ` FROM restaurants HAVING distance <= ${radius} ORDER BY distance ASC`
    console.log(query)
  
  Sql.query(query, (error, result, fields) => {
        if (!error) {
            res.json(result)
        } else {
            res.json(error)
        }
        
    });
    
});

router.get('/feed/location', function(req, res, next) {
  
  res.json([{
    name: 'hello'  
  }]);
});


module.exports = router;
