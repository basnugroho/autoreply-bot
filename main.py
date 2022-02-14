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
phone = '6282141421214'
first_line = ""
with open("session.txt", "r") as file:
    first_line = file.readline()
    for last_line in file:
        pass
print(first_line)
session_file = first_line #use your username if unsure

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

    cuti = True
    cuti_from = "2021-12-7"
    cuti_until = "2021-12-8"

    users = []
    known_users = ['']
    rochdff_df = pd.read_excel('./ROC HD FF.xlsx')
    cuti = False

    # function to get unique values
    def unique(list1):
    
        # initialize a null list
        unique_list = []
        
        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        # return unique list
        print(unique_list)
        return unique_list

    # @client.on(events.NewMessage(incoming=True))
    # async def handle_new_message(event):
    #     if event.is_private and cuti==True:  # only auto-reply to private chats
    #         from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
    #         if not from_.bot:  # don't auto-reply to bots
    #             # print(time.asctime(), '-', event.message)  # optionally log time and message
    #             time.sleep(1)  # pause for 1 second to rate-limit automatic replies
    #             # result = await client(SendMessageRequest(await client.get_input_entity('username'), 'Hello there!'))
    #             found = 0
    #             for i, user in enumerate(users):
    #                 if user == users[i] and cuti:
    #                     found += 1
    #             if found == 0:
    #                 await event.respond(f"**[AUTO REPLY]** \nBapak/Ibu/Kakak __@{from_.username}__. Mohon maaf saya sedang **cuti** hingga **{cuti_until}** 🏖⏳ \nJika urgent silahkan call telegram ini 🙏🙂")
    #                 users.append(from_.username)

    # @client.on(events.NewMessage(incoming=True))
    # async def handle_new_message(event):
    #     if event.is_private and cuti==True:  # only auto-reply to private chats
    #         from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
    #         if not from_.bot:  # don't auto-reply to bots
    #             # print(time.asctime(), '-', event.message)  # optionally log time and message
    #             time.sleep(1)  # pause for 1 second to rate-limit automatic replies
    #             # result = await client(SendMessageRequest(await client.get_input_entity('username'), 'Hello there!'))
    #             found = 0
    #             for i, user in enumerate(users):
    #                 if user == users[i] and cuti:
    #                     found += 1
    #             if found == 0:
    #                 await event.respond(f"**[AUTO REPLY]** \nBapak/Ibu/Kakak __@{from_.username}__. Mohon maaf saya sedang **cuti** hingga **{cuti_until}** 🏖⏳ \nJika urgent silahkan call telegram ini 🙏🙂")
    #                 users.append(from_.username)

    # fu woc
    @client.on(events.NewMessage(pattern='(?i)fu|woc|fu woc'))
    async def handler(event):
        if event.is_private:  # only auto-reply to private chats
            # print("event: "+event.message)
            chat = str(event.message.message)
            message_splitted = chat.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]
            witels = ['denpasar', 'jember', 'kediri', 'madiun', 'madura', 'malang', 'ntb', 'ntt', 'pasuruan', 'surabaya selatan', 'surabaya utara',
                    'sidoarjo', 'singaraja']
            from_ = await event.client.get_entity(event.from_id)
            if not from_.bot and len(message_splitted) > 0:
                await event.respond(f"**[AUTO REPLY]** Memproses ke ROC HD FF.")
            usernames = [] 
            destination = "ROC - HD FF WOC REG5"   
            for message in message_splitted:
                for witel in witels:
                    if witel in message.lower():
                        username = rochdff_df.loc[rochdff_df['witel'] == witel]['Username'].item()
                        # for sending instead of printing
                        pesan = re.sub("fu\s+\w+\s+\w+", "", message)
                        moban = f"{pesan}. Moban rekan di WITEL {witel.upper()} {username}. Terima Kasih 🙏\n"
                        # await event.respond(moban)
                        await client.send_message(destination, moban)
                        await event.respond(f"pesan untuk rekan di WITEL {witel.upper()} {username}. terkirim 👌")
                        usernames.append(username)
            await event.respond(f"jika terdapat kesalahan data mohon koreksi 🙏")
            # await client.send_message(destination, f"rekan-rekan, jika terdapat kesalahan data mohon koreksi 🙏\n\ncc: {', '.join(unique(usernames))}")
            await client.send_message(destination, f"jika terdapat kesalahan atau ada update data mohon japri 🙏")
            await event.respond("done 💯")
    
    # gladius
    @client.on(events.NewMessage(pattern='(?i)Your OTP Code User 930436 is'))
    async def handler(event):
        peer_id = str(event.message.peer_id)
        peer_id = int(re.findall('[0-9]+', peer_id)[0])
        if event.is_private and peer_id==1448100713:  # only auto-reply to private chats
            print("gladius OTP request")
            print(peer_id)

            requester = 'Internal Fallout NOSS-F Solution'
            moban = str(event.message.message)
            message_splitted = moban.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]

            await client.send_message(requester, f"[OTP Gladius 📩 {requester}]")
            await client.send_message(requester, moban)
            pesan = """Harap diperhatikan checklist berikut sebelum create radius/pcrf di gladius:
1. cek apakah termasuk no. Fraud di bot @telkom_roc5_bot, 
format: 
/cekfraud no_inet (bisa langsung banyak nomor)
2. cek NCX apakah masih aktif / tidak
3. cek di UIM nya ada service aktif / tidak"""
            await client.send_message(requester, pesan)
            await event.respond(f"forwarded to {requester} 💯")

    # kpro
    @client.on(events.NewMessage(pattern='(?i)Your OTP Code is'))
    async def handler(event):
        peer_id = str(event.message.peer_id)
        peer_id = int(re.findall('[0-9]+', peer_id)[0])
        if event.is_private and peer_id==1298139737:  # only auto-reply to private chats
            print("KPRO OTP request")
            print(peer_id)

            requester = 'Internal Fallout NOSS-F Solution'
            moban = str(event.message.message)
            message_splitted = moban.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]

            await client.send_message(requester, f"[OTP KPRO 📩 {requester}]")
            await client.send_message(requester, moban)
            await event.respond(f"forwarded to {requester} 💯")
        else:  # only auto-reply to private chats
            print("Dashboard FF OTP request")
            print(peer_id)

            requester = 'Internal Fallout NOSS-F Solution'
            moban = str(event.message.message)
            message_splitted = moban.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]

            await client.send_message(requester, f"[OTP Dashboard FF 📩 {requester}]")
            await client.send_message(requester, moban)
            await event.respond(f"forwarded to {requester} 💯")

    # uimtools
    @client.on(events.NewMessage(pattern='(?i)Your OTP for uimtools is'))
    async def handler(event):
        peer_id = str(event.message.peer_id)
        peer_id = int(re.findall('[0-9]+', peer_id)[0])
        if event.is_private and peer_id==1124477729:  # only auto-reply to private chats
            print("uimtools OTP request")
            print(peer_id)

            requester = 'Internal Fallout NOSS-F Solution'
            moban = str(event.message.message)
            message_splitted = moban.split('\n')
            message_splitted = [re.sub(r'\s+', ' ', message) for message in message_splitted]

            await client.send_message(requester, f"[OTP UIMTOOLS 📩 {requester}]")
            await client.send_message(requester, moban)
            await event.respond(f"forwarded to {requester} 💯")

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
            destination = "TR5 - FALLOUT UIM"
            sbu_fallout_group = "FALLOUT DATA SBU"
            from_ = await event.client.get_entity(event.from_id)
            if not from_.bot and len(message_splitted) > 0:
                for message in message_splitted:
                    for witel in witels:
                        if witel in message.lower():
                            message = re.sub("eskalasi\s+\w+\s+\w+", "", message)
                            if "utara" in message.lower():
                                if "#cons" in message.lower():
                                    await event.respond(f"**[AUTO REPLY]** Memproses ke {sbu_fallout_group}")
                                    await event.respond(f"mantap yang SBU udah sesuai format!")
                                    await client.send_message("FALLOUT DATA SBU", message)
                                    await event.respond(f"Pesan untuk {witels[witel]} di {witel.upper()} terkirim 👌")
                                else:
                                    await event.respond(f"""Ups! Fallout SBU Found dan tidak sesuai format! Mohon berikan format seperti contoh berikut:\n\n#FALLOUT #CONS SC520196200 Tiket : IN122116759_2|Error=1057:Service_Port is missing for 53668992_152403202135_INTERNET 🙏""")
                            elif "#cons" in message.lower():
                                await event.respond(f"**[AUTO REPLY]** Memproses ke {sbu_fallout_group}")
                                await event.respond(f"mantap yang SBU udah sesuai format!")
                                await client.send_message("FALLOUT DATA SBU", message)
                                await event.respond(f"Pesan untuk {witels[witel]} di {witel.upper()} terkirim 👌")
                            else:
                                await event.respond(f"**[AUTO REPLY]** Memproses ke {destination}")
                                await client.send_message(destination, f"Semangat Pagi! Moban {witels[witel]} di {witel.upper()} \n{message} Terima Kasih 🙏\n")
                                await event.respond(f"Pesan untuk {witels[witel]} di {witel.upper()} terkirim 👌")
                                usernames.append(witels[witel])
            await event.respond(f"jika terdapat kesalahan data mohon koreksi 🙏")
            # await client.send_message(destination, f"bapak/ibu/rekan, jika terdapat kesalahan data mohon koreksi 🙏\n\ncc: {', '.join(unique(usernames))}")

    @client.on(events.NewMessage(pattern='(?i)cancel|CANCEL'))
    async def cancel_to_cc(event):
        if event.is_private:  # only auto-reply to private chats
            message = str(event.message.message)
            from_ = await event.client.get_entity(event.from_id)
            if not from_.bot:
                await event.respond(f"**[AUTO REPLY]** Memproses ke CC TR5.")
            message = f"**[AUTO FORWARDER]**\n\n{message}"
            await client.send_message("irttyo", message)
            await event.respond("done 💯")

    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone)
    # list all sessions
    print(client.session.list_sessions())

    # delete current session (current session is associated with `username` variable)
    # client.log_out()
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')
