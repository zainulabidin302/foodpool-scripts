
var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '000000',
  database : 'foodpool'
});



module.exports = connection;
