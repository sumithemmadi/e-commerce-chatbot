import { Boom } from '@hapi/boom';
import NodeCache from 'node-cache';
import makeWASocket, {
   AnyMessageContent,
   delay,
   fetchLatestBaileysVersion,
   makeInMemoryStore,
   DisconnectReason,
   proto,
   useMultiFileAuthState,
   WAMessageContent,
   WAMessageKey,
   getAggregateVotesInPollMessage,
} from '@whiskeysockets/baileys';

const msgRetryCounterCache = new NodeCache();

class WhatsApp {
   sock: any;
   store: any;
   registration: any;

   constructor() {
      this.store = makeInMemoryStore({});
      this.store?.readFromFile('./baileys_store_multi.json');
      setInterval(() => {
         this.store?.writeToFile('./baileys_store_multi.json');
      }, 10_000);
   }

   async initializeWhatsApp() {
      const { state, saveCreds } = await useMultiFileAuthState('baileys_auth_info');
      const { version, isLatest } = await fetchLatestBaileysVersion();
      console.log(`using WA v${version.join('.')}, isLatest: ${isLatest}`);

      this.sock = makeWASocket({
         version,
         printQRInTerminal: true,
         auth: state,
         msgRetryCounterCache,
         generateHighQualityLinkPreview: true,
         syncFullHistory: true,
         getMessage: this.getMessage,
      });

      this.store?.bind(this.sock.ev);

      this.sock.ev.process(async (events: any) => {
         if (events['connection.update']) {
            const update = events['connection.update'];
            const { connection, lastDisconnect } = update;
            if (connection === 'close') {
               if (
                  (lastDisconnect?.error as Boom)?.output?.statusCode !== DisconnectReason.loggedOut
               ) {
                  this.initializeWhatsApp();
               } else {
                  console.log('Connection closed. You are logged out.');
               }
            }

            console.log('connection update', update);
         }
         if (events['creds.update']) {
            await saveCreds()
         }

         // if (events['messages.upsert']) {
         //    const upsert = events['messages.upsert']
         //    console.log('recv messages ', JSON.stringify(upsert, undefined, 2))

         //    if (upsert.type === 'notify') {
         //       for (const msg of upsert.messages) {
         //          if (!msg.key.fromMe) {
         //             console.log('replying to', msg.key.remoteJid)
         //             await this.sock!.readMessages([msg.key])
         //             await this.sendMessageWTyping({ text: 'Hello there!' }, msg.key.remoteJid!)
         //          }
         //       }
         //    }
         // }

         // // messages updated like status delivered, message deleted etc.
         // if (events['messages.update']) {
         //    console.log(
         //       JSON.stringify(events['messages.update'], undefined, 2)
         //    )

         //    for (const { key, update } of events['messages.update']) {
         //       if (update.pollUpdates) {
         //          const pollCreation = await this.getMessage(key)
         //          if (pollCreation) {
         //             console.log(
         //                'got poll update, aggregation: ',
         //                getAggregateVotesInPollMessage({
         //                   message: pollCreation,
         //                   pollUpdates: update.pollUpdates,
         //                })
         //             )
         //          }
         //       }
         //    }
         // }

         // if (events['message-receipt.update']) {
         //    console.log(events['message-receipt.update'])
         // }


      });
   }

   async sendMessageWTyping(msg: AnyMessageContent, jid: string) {
      await this.sock.presenceSubscribe(jid);
      await delay(500);

      await this.sock.sendPresenceUpdate('composing', jid);
      await delay(2000);

      await this.sock.sendPresenceUpdate('paused', jid);

      await this.sock.sendMessage(jid, msg);
   }

   async getMessage(key: WAMessageKey): Promise<WAMessageContent | undefined> {
      if (this.store) {
         const msg = await this.store.loadMessage(key.remoteJid!, key.id!);
         return msg?.message || undefined;
      }

      return proto.Message.fromObject({});
   }

   async getReadReceipts(key: WAMessageKey): Promise<WAMessageContent | undefined> {
      if (this.store) {
         const msg = await this.store.loadMessage(key.remoteJid!, key.id!);
         return msg?.userReceipt || undefined;
      }

      return proto.Message.fromObject({});
   }


}

export { WhatsApp };
