
var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '000000',
  database : 'fp_new'
});



module.exports = connection;
