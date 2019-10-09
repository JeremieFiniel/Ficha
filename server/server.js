var net = require('net');
var fs = require('fs');

var server = net.createServer(function (socket) {
	console.log('new client connected : %s', socket.remoteAddress);

	state = 'connected';
	filename = "Unknow";
	socket.on('data', function(data) {
		if (state == 'connected')
		{
			filename = data.toString();
			console.log("filename : %s", filename);
			state = 'download';
		}
		else if (state == 'download')
			fs.appendFileSync(filename, data, 'binary');
	});
	socket.on('close', function() {
		console.log('connection closed');
	});
});

server.listen(8123, "", function() {
	console.log('listen');
});
