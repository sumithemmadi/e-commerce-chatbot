import express from 'express';
import { Application } from 'express';
import { WhatsApp } from './whatsapp';
import { WAMessageKey } from '@whiskeysockets/baileys';
import { Server, Socket } from 'socket.io';
import { createServer } from 'node:http';

// express
const app: Application = express();
app.use(express.json());
const port = 3000;

// socket.io
const server = createServer(app);
const io = new Server(server);

// baileys
const whatsappClient = new WhatsApp();
whatsappClient.initializeWhatsApp();


app.post('/api/get-read-receipts', async (req, res) => {
   const { key } = req.body;
   if (!key) {
      res.status(400).json({
         success: false,
         message: 'Missing key in the request body',
      });
   }

   try {
      const messageData = await whatsappClient.getReadReceipts(key);
      res.status(200).json({
         success: true,
         timestamp: Date.now(),
         readReceipts: messageData
      });
   } catch (error: any) {
      res.status(500).json({
         success: true,
         message: 'Internal Server Error',
      });
   }
});


io.on('connection', async (socket: Socket) => {
   socket.on('message-read-receipts', async (key: WAMessageKey) => {
      try {
         let mdata = await whatsappClient.getReadReceipts({
            remoteJid: "919010118054-1567096861@g.us",
            fromMe: true,
            id: "E85398F69A6DE2F5288F57543B5AAA26",
            participant: "919912857147@s.whatsapp.net"

         });
         io.emit('message', JSON.stringify({
            success: true,
            timestamp: Date.now(),
            readReceipts: mdata
         }, null, 3));

      } catch (error: any) {
         io.emit('message', JSON.stringify({
            success: false,
            timestamp: Date.now(),
            message: "Error occured",
            errorMessage: error.message
         }));
      }

   });
});


server.listen(port, () => {
   console.log(`Server is running on http://localhost:${port}`);
});
