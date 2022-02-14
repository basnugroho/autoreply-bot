from telethon.sync import TelegramClient
from telethon import functions, types

# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Tele>
# or use your own
api_id = 1200750
api_hash = '7970f21bf68122b9ad71f698092a7650'

# fill in your own details here
phone = '6282141421214'
session_file = 'ff-roc-local'  # use your username if unsure

with TelegramClient(session_file, api_id, api_hash) as client:
    result = client(functions.account.ResetAuthorizationRequest(hash=-12398745604826))
print(result)
