import { Boom } from '@hapi/boom';
import NodeCache from 'node-cache';
import makeWASocket, {
    AnyMessageContent,
    delay,
    DisconnectReason,
    fetchLatestBaileysVersion,
    makeInMemoryStore,
    proto,
    useMultiFileAuthState,
    WAMessageContent,
    WAMessageKey,
} from '@whiskeysockets/baileys';
import axios from 'axios';

const msgRetryCounterCache = new NodeCache();

const store = makeInMemoryStore({});

store?.readFromFile('./baileys_store_multi.json');
setInterval(() => {
    store?.writeToFile('./baileys_store_multi.json');
}, 10_000);

const startSock = async () => {
    const { state, saveCreds } = await useMultiFileAuthState('baileys_auth_info');
    const { version, isLatest } = await fetchLatestBaileysVersion();
    console.log(`using WA v${version.join('.')}, isLatest: ${isLatest}`);

    const sock = makeWASocket({
        version,
        printQRInTerminal: true,
        auth: state,
        msgRetryCounterCache,
        generateHighQualityLinkPreview: true,
        getMessage,
        syncFullHistory: true,
    });

    store?.bind(sock.ev);

    const sendMessageWTyping = async (msg: AnyMessageContent, jid: string) => {
        await sock.presenceSubscribe(jid);
        await delay(500);

        await sock.sendPresenceUpdate('composing', jid);
        await delay(2000);

        await sock.sendPresenceUpdate('paused', jid);

        await sock.sendMessage(jid, msg);
    };

    sock.ev.process(async (events) => {
        if (events['connection.update']) {
            const update = events['connection.update'];
            const { connection, lastDisconnect } = update;
            if (connection === 'close') {
                if (
                    (lastDisconnect?.error as Boom)?.output?.statusCode !== DisconnectReason.loggedOut
                ) {
                    startSock();
                } else {
                    console.log('Connection closed. You are logged out.');
                }
            }

            console.log('connection update', update);
        }
        if (events['creds.update']) {
            await saveCreds()
        }
        if (events['messages.upsert']) {
            const upsert = events['messages.upsert']
            console.log('recv messages ', JSON.stringify(upsert, undefined, 2))

            if (upsert.type === 'notify') {
                for (const msg of upsert.messages) {
                    if (!msg.key.fromMe) {
                        const data = {
                            phoneNumber: msg.key.remoteJid,
                            message: msg.message?.conversation
                        };

                        try {
                            const response = await axios.post('http://localhost:5000/api', data);
                            console.log('Response:', response.data);

                            console.log('replying to', msg.key.remoteJid);
                            await sock!.readMessages([msg.key]);
                            await sendMessageWTyping({ text: response.data.message }, msg.key.remoteJid!);
                        } catch (error) {
                            console.error('Error:', error);
                        }
                    }
                }
            }
        }
    });

    return { sock, store };

    async function getMessage(key: WAMessageKey): Promise<WAMessageContent | undefined> {
        if (store) {
            const msg = await store.loadMessage(key.remoteJid!, key.id!);
            return msg?.message || undefined;
        }


        return proto.Message.fromObject({});
    }
};
