import time
import re
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest
from telethon import utils
import pandas as pd
from telethon.sync import TelegramClient
from telethon import functions, types
from datetime import datetime

# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
api_id = 18595913
api_hash = '91f0334687c83a3a1fba46c513d57eb1'

# fill in your own details here
phone = '6285156595540'
first_line = ""
with open("session.txt", "r") as file:
    first_line = file.readline()
    for last_line in file:
        pass
print("session name: "+first_line)
session_file = "ffroc5" #use your username if unsure

with TelegramClient(session_file, api_id, api_hash) as client:
    result = client(functions.account.ResetAuthorizationRequest(hash=-12398745604826))
print(result)

if __name__ == '__main__':
    # Create the client and connect
    # use sequential_updates=True to respond to messages one at a time
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)
    client.connect()

    # forward kawalorder
    @client.on(events.NewMessage(incoming=True))
    async def kawal_order(event):
        peer_id = str(event.message.peer_id)
        peer_id = int(re.findall('[0-9]+', peer_id)[0])
        if event.is_private == False:
            if  204353928 == peer_id:
                # write
                f = open("ff_message_log.txt", "a")
                f.write("time: "+str(datetime.now())+", ")
                f.write("peer id: "+str(peer_id)+", ")
                origin = "ROC - HD FF WOC REG5"
                destination = "Internal Fallout NOSS-F Solution"
                
                record_messages(event)
                if "@fftreg5" in event.message.message and "#kawalorder" in event.message.message:
                    pesan = str(event.message.message)
                    order_id = "SC"+re.findall(r'\d+', pesan)[0]
                    no_tiket = "R"+"SC"+re.findall(r'\d+', pesan)[1]
                    print("no ticket: "+no_tiket)
                    await event.respond(f"siap! order id: {order_id} dengan no. ticket: {no_tiket} on process kawan 😊")
                    await client.send_message(destination, f"[KAWALORDER], moban eskalasi order id: {order_id} dengan no. ticket: {no_tiket} berikut gaes! 😊")
                    await client.send_message(destination, pesan);print(pesan)
                elif "@fftreg5" in event.message.message and "#kawalorder" not in event.message.message:
                    pesan = str(event.message.message);print(pesan)
                    await event.respond(f"""Maaf! Mohon ulangi pesan di atas dengan prefix #kawalorder di dalam satu message agar dikenali sistem 🙏

                    contoh:
                    #kawalorder
                    SIstem Proaktif Reaktif Incident MAnagement 
                    Order ID = SC522485126
                    SEGMEN = 
                    No Ticket = R2022030700536
                    Tanggal Masuk = 2022-03-07 14:48:44
                    Username Pelapor = komangsurahardja
                    Nama Pelapor = komang-surahardja 
                    Nama Tier1 = 
                    Nama Tier2 = Indah Hermina
                    Tanggal Selesai = 
                    Lesson Learned = Tiket Sedang Proses Pengecekan
                    Deskripsi = SOM-ID:425860064 TOM-ID:425185824 MOBANTFO moban TFO ganti ont 

                    SC522485126
                    SOM: 425860064 GetTechnicalOrderTask
                    TOM: 425185824 ValidateWFM
                    WFM ID 275801265 VALSTART

                    Mohon bantuan eskalasi percepatan rekan @fftreg5 lokasi pelanggan cukup jauh diluar kota🙏""")

    # record log
    def record_messages(event):
        peer_id = str(event.message.peer_id)
        peer_id = int(re.findall('[0-9]+', peer_id)[0])
        # write
        f = open("ff_message_log.txt", "a")
        f.write("time: "+str(datetime.now())+", ")
        f.write("peer id: "+str(peer_id)+", ")
        group = ""
        if  1273072077 == peer_id:
            group = "Kawal FF-DIT"
        elif  1080681328 == peer_id:
            group = "ROC - HD FF WOC REG5"
        elif 1273072077 == peer_id:
            group = "Kawal FF-DIT"
        else:
            group = ""
        f.write(f"group: {group}, ")
        f.write("message: "+str(event.message.message)+", ")
        f.write("event_message: "+str(event.message)+"\n")
        f.close()
        # read
        with open("ff_message_log.txt", "r") as file:
            for last_line in file:
                pass
        print(last_line)
        file.close()

    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone)
    # list all sessions
    print(client.session.list_sessions())
    print("")

    # delete current session (current session is associated with `username` variable)
    # client.log_out()
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')