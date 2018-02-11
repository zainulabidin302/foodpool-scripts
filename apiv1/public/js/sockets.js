var ws = new WebSocket('ws://localhost:3000');

console.log(ws);
console.log('hello owled')
var toMsg = (msg) => JSON.stringify(msg)
var fromMsg = (msg) => JSON.parse(msg.data)


ws.onopen = () => {
    var message = {
        connection: 'open'
    }
    ws.send(toMsg(message));
};


ws.onmessage = (message) => {
    console.log('recieved response!', fromMsg(message))
}

ws.onerror = (message) => {
    console.log('error response!', console.log(message))
}