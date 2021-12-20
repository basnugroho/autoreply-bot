import time
import re
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import SendMessageRequest
from telethon import utils
import pandas as pd
from telethon.sync import TelegramClient
from telethon import functions, types
from datetime import datetime
from flask import jsonify


# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
api_id = 1200750
api_hash = '7970f21bf68122b9ad71f698092a7650'

# fill in your own details here
phone = '6282141421214'
session_file = 'ff-roc'  # use your username if unsure

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

    cuti = False
    cuti_from = "2021-12-7"
    cuti_until = "2021-12-8"

    users = []
    known_users = ['']
    rochdff_df = pd.read_excel('./ROC HD FF.xlsx')
    cuti = False

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        if event.is_private and cuti==True:  # only auto-reply to private chats
            from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
            if not from_.bot:  # don't auto-reply to bots
                # print(time.asctime(), '-', event.message)  # optionally log time and message
                time.sleep(1)  # pause for 1 second to rate-limit automatic replies
                # result = await client(SendMessageRequest(await client.get_input_entity('username'), 'Hello there!'))
                found = 0
                for i, user in enumerate(users):
                    if user == users[i] and cuti:
                        found += 1
                if found == 0:
                    await event.respond(f"**[AUTO REPLY]** \nBapak/Ibu/Kakak __@{from_.username}__. Mohon maaf saya sedang **cuti** hingga **{cuti_until}** 🏖⏳ \nJika urgent silahkan call telegram ini 🙏🙂")
                    users.append(from_.username)

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        if event.is_private and cuti==True:  # only auto-reply to private chats
            from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
            if not from_.bot:  # don't auto-reply to bots
                # print(time.asctime(), '-', event.message)  # optionally log time and message
                time.sleep(1)  # pause for 1 second to rate-limit automatic replies
                # result = await client(SendMessageRequest(await client.get_input_entity('username'), 'Hello there!'))
                found = 0
                for i, user in enumerate(users):
                    if user == users[i] and cuti:
                        found += 1
                if found == 0:
                    await event.respond(f"**[AUTO REPLY]** \nBapak/Ibu/Kakak __@{from_.username}__. Mohon maaf saya sedang **cuti** hingga **{cuti_until}** 🏖⏳ \nJika urgent silahkan call telegram ini 🙏🙂")
                    users.append(from_.username)

    @client.on(events.NewMessage(pattern='(?i)idem|ggn|selamat|lambat'))
    async def handle_messages(event):
        try:
            print(event)
            print("\nsending....")
            destination = "roc5_unofficial"
            messages = str(event.message).split(",")
            for mess in messages:
                if "None" not in mess:
                    await client.send_message(destination, str(mess))
            print("done\n")
        except Exception as e:
            print("Error:", e)



    @client.on(events.NewMessage(pattern='(?i)fu|woc|fu woc'))
    async def fu_roc_hd_ff(event):
        if event.is_private:  # only auto-reply to private chats
            chat = str(event.message.message)
            message_splitted = chat.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]
            witels = ['denpasar', 'jember', 'kediri', 'madiun', 'madura', 'malang', 'ntb', 'ntt', 'pasuruan', 'surabaya selatan', 'surabaya utara',
                    'sidoarjo', 'singaraja']
            from_ = await event.client.get_entity(event.from_id)
            if not from_.bot and len(message_splitted) > 0:
                await event.respond(f"**[AUTO REPLY]** Memproses ke ROC HD FF.")
            usernames = []
            for message in message_splitted:
                for witel in witels:
                    if witel in message.lower():
                        username = rochdff_df.loc[rochdff_df['witel'] == witel]['Username'].item()
                        # for sending instead of printing
                        # pesan = pesan = re.sub("fu\s+\w+\s+\w+", "", message)
                        moban = f"{message}. Moban rekan di WITEL {witel.upper()} {username}. Terima Kasih 🙏\n"
                        usernames.append(username)
                        await event.respond(moban)
                        await client.send_message("ROC - HD FF WOC REG5", moban)
	    # destination_group_invite_link="https://t.me/+DC4xiLUfyBgknY8z"                        
        #     entity=client.get_entity(destination_group_invite_link)	    
        #     await client.send_message(entity, moban)
            await event.respond(f"jika terdapat kesalahan data mohon koreksi 🙏")
            await client.send_message("ROC - HD FF WOC REG5", f"jika terdapat kesalahan data mohon japri 🙏\ncc: {', '.join(usernames)}")
            #await client.send_message("https://t.me/+DC4xiLUfyBgknY8z", f"jika terdapat kesalahan atau ada update data mohon japri 🙏")
            await event.respond("done 💯")

    @client.on(events.NewMessage(pattern='(?i)daman|uim'))
    async def forward_daman(event):
        if event.is_private:  # only auto-reply to private chats
            message = str(event.message.message)
            message_splitted = message.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]

            witels = {'denpasar': 'Pak @elankusuma', 
            'jember': 'Bu @ikariny', 
            'kediri': 'Bu @ITA_RETNO',
            'madiun': 'Pak @ryandwiardianto', 
            'madura': 'Mbak @fijrahasri',
            'malang': 'Pak @ChandraPoetra',
            'ntb': 'Mas @masfiuuu', 
            'ntt': 'Bu @jaywny', 
            'pasuruan': 'Pak @damanmoni', 
            'surabaya selatan': 'Bu @yayukfitriana', 
            'surabaya utara': 'Grup Fallout DATA SBU Pak @w1d0d0',
            'sidoarjo': 'Sam @andrewnugroho', 
            'singaraja': 'Pak @dex_suardhana'
            }

            usernames = []
            from_ = await event.client.get_entity(event.from_id)
            if not from_.bot and len(message_splitted) > 0:
                await event.respond(f"**[AUTO REPLY]** Memproses ke TR5 - FALLOUT UIM.")
            for message in message_splitted:
                for witel in witels:
                    if witel in message.lower():
                        message = re.sub("eskalasi\s+\w+\s+\w+", "", message)
                        await event.respond(f"Semangat Pagi! Moban {witels[witel]} di {witel.upper()} \n{message} Terima Kasih 🙏\n")
                        await client.send_message("TR5 - FALLOUT UIM", f"Semangat Pagi! Moban {witels[witel]} di {witel.upper()} \n{message} Terima Kasih 🙏\n")
                        usernames.append(witels[witel])
            await event.respond(f"jika terdapat kesalahan data mohon koreksi 🙏")
            await client.send_message("TR5 - FALLOUT UIM", f"jika terdapat kesalahan data mohon japri 🙏\ncc: {', '.join(usernames)}")


    @client.on(events.NewMessage(pattern='(?i)cancel|CANCEL'))
    async def cancel_to_cc(event):
        if event.is_private:  # only auto-reply to private chats
            message = str(event.message.message)
            from_ = await event.client.get_entity(event.from_id)
            if not from_.bot:
                await event.respond(f"**[AUTO REPLY]** Memproses ke CC TR5.")
            message = f"**[AUTO FORWARDER]**\n\n{message}"
            destination = "irttyo"
            await client.send_message(destination, message)
            await client.send_message(f"processed to {destination}: message")
            await event.respond("done 💯")
    
    # @client.on(events.NewMessage(chats = "Kawal FF-DIT"))
    # async def my_event_handler(event):
    #     print(event.raw_text)

    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone)
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')
