var mysql = require('./mysql');

var log_activity = (params) => {
    var _query = 'INSERT INTO `user_activity_log` (user_id, endpoint, guest, note) VALUES (?, ?, ?, ?)';
    mysql.query(_query, params, (e, r, f) => {
      if (e)
        conosle.log(e)
    });
  }
  
  
  module.exports = {
    log_activity: log_activity
  }