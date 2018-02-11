var url = require('url')

var onMessage = (ws) => {
    return (message) => {
        ws.send(JSON.stringify({
            'connection': 'open'
        }))
    }
}

var onError = (err) => {
    console.log(err)
}

var onConnection = (ws, req) => {
    const location = url.parse(req.url, true);
    // You might use location.query.access_token to authenticate or share sessions
    // or req.headers.cookie (see http://stackoverflow.com/a/16395220/151312)
    ws.on('message', onMessage(ws));
    ws.on('error', onError);
}

module.exports = {
    onMessage: onMessage,
    onError: onError,
    onConnection: onConnection
}