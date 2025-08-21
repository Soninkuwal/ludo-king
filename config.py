#API_ID = "YOUR_API_ID"
#API_HASH = "YOUR_API_HASH"
#BOT_TOKEN = "YOUR_BOT_TOKEN"

# Put Telegram user IDs of all admins
#ADMINS = [123456789, 987654321]

#OWNER_ID = 123456789



# Don't Remove Credit Tg - @SONICKUWALSSCBOT
# website For Amazing Bot https://sonickuwalssc.blogspot.com/
# Ask Doubt on telegram @SONICKUWALUPDATEKANHA

from os import environ

API_ID = environ.get("API_ID", "")
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

# Put Telegram user IDs of all admins
#ADMINS = [123456789, 987654321]
ADMINS = environ.get("ADMINS", )
OWNER_ID = environ.get("OWNER_ID", "")

