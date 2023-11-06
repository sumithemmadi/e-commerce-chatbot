import io from 'socket.io-client';
const socket = io('http://localhost:3000');

socket.on('connect', () => {
    socket.emit('message-read-receipts',
        {
            remoteJid: "919010118054-1567096861@g.us",
            fromMe: true,
            id: "E85398F69A6DE2F5288F57543B5AAA26",
            participant: "919912857147@s.whatsapp.net"

        }
    );
});

socket.on('message', (data) => {
    console.log('Received message:', JSON.stringify(JSON.parse(data),null,3));
});

socket.on('disconnect', () => {
    console.log('Disconnected from the server');
});
