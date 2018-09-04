var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('express-session')
var MySQLStore = require('connect-mysql')(session);

var options = {
  config: {
    user: 'root', 
    password: '', 
    database: 'fp_new' 
  }
};

var index = require('./routes/index');
var users = require('./routes/users');

var app = express();


// session setup

app.use(session({
  secret: 'v;kqwp4j}',
  resave: false,
  store: new MySQLStore(options),
  saveUninitialized: true,
}))





// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(function (req, res, next) {

  // Website you wish to allow to connect
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8100');

  // Request methods you wish to allow
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

  // Request headers you wish to allow
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Set to true if you need the website to include cookies in the requests sent
  // to the API (e.g. in case you use sessions)
  res.setHeader('Access-Control-Allow-Credentials', true);

  // Pass to next layer of middleware
  next();
});



app.use(function(req, res, next) {
  console.log('req.path', req.path, req.sessionID)
  if (req.session.logged_in && req.session.logged_in == true) {
    next()  
  } else if (req.path == '/users/auth') {
    next()
  } else {
    if (req.method.toLowerCase() == 'get') {
      res.render('unauth')
    } else {
      return res.json({
        error: 'unauthorized'
      })
    }
  }
})



app.use('/', index);
app.use('/users', users);
// cors





// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});











module.exports = app;
