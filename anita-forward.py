import time
import re
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest
from telethon import utils
import pandas as pd
from telethon.sync import TelegramClient
from telethon import functions, types


# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
api_id = 9380480
api_hash = 'f3d8f3bf880eec1db6a52a37ef22e2ed'

# fill in your own details here
phone = '6285331899365'
session_file = 'anita'  # use your username if unsure

with TelegramClient(session_file, api_id, api_hash) as client:
    result = client(functions.account.ResetAuthorizationRequest(hash=-12398745604826))
print(result)

# content of the automatic reply
message = "**[AUTO REPLY]** \nMohon maaf, saya sedang cuti hingga 8-12-2021. Jika urgent silahkan call 🙏😄"

if __name__ == '__main__':
    # Create the client and connect
    # use sequential_updates=True to respond to messages one at a time
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)
    client.connect()

    # kpro
    @client.on(events.NewMessage(pattern='(?i)Your OTP Code is'))
    async def handler(event):
        if event.is_private:  # only auto-reply to private chats
            print("kpro OTP request")
            print(event)
            #print(str(event.message))
            peer_id = str(event.message.peer_id)
            print(f"peer_id: {peer_id}")
            peer_id = int(re.findall('[0-9]+', peer_id)[0])
            print(peer_id)
            # peers = {'Internal Fallout NOSS-F Solution': 1298139737, 'RangerFF': 1448100713}
            # requester = ""
            # for key, value in peers.items():
            #     if peer_id == value:
            #         requester = key
            #         print("requester: "+requester)
            #         break
            # if requester == "":
            #     print(f"requester unknown, peer_id {peer_id}")
            requester = 'Internal Fallout NOSS-F Solution'
            moban = str(event.message.message)
            message_splitted = moban.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]

            await client.send_message(requester, f"[AUTO FORWARD OTP KPRO or Dashboard FF to {requester}]")
            await client.send_message(requester, moban)
            await event.respond(f"forwarded to {requester} 💯")

    # uimtools
    @client.on(events.NewMessage(pattern='(?i)Your OTP for uimtools is'))
    async def handler(event):
        if event.is_private:  # only auto-reply to private chats
            print("kpro OTP request")
            print(event)
            #print(str(event.message))
            peer_id = str(event.message.peer_id)
            print(f"peer_id: {peer_id}")
            peer_id = int(re.findall('[0-9]+', peer_id)[0])
            print(peer_id)

            requester = 'Internal Fallout NOSS-F Solution'
            moban = str(event.message.message)
            message_splitted = moban.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]

            await client.send_message(requester, f"[AUTO FORWARD OTP UIMTOOLS to {requester}]")
            await client.send_message(requester, moban)
            await event.respond(f"forwarded to {requester} 💯")

    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone)
    # list all sessions
    print(client.session.list_sessions())

    # delete current session (current session is associated with `username` variable)
    # client.log_out()
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')
