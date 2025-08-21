import os
import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import create_tables, add_user
import config

# For Koyeb/Render/Heroku compatibility (not strictly required for polling, but no harm)
PORT = int(os.environ.get("PORT", 8080))

app = Client("ludo_king_bot",
             api_id=config.API_ID,
             api_hash=config.API_HASH,
             bot_token=config.BOT_TOKEN)

create_tables()

START_BTN = InlineKeyboardMarkup([
    [InlineKeyboardButton("Join Ludo Table", callback_data="join_table")],
    [InlineKeyboardButton("Help", url="https://t.me/your_channel")],
    [InlineKeyboardButton("Contact Admin", url="https://t.me/admin_username")]
])

#@app.on_message(filters.command("start") & filters.private)
#async def start(client, message):
#    thumb = "start_thumb.jpg"
#    await message.reply_photo(
#        thumb,
#        caption="Welcome to Ludo King Bot! Play and Win.\nJoin a match, send /wallet to check balance.",
#        reply_markup=START_BTN
#    )

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_photo(
        "https://graph.org/file/cfd480c2bdb7b3d2f44a1-bd93c08bfa2255ed9b.jpg",
        caption="Welcome to Ludo King Bot! Play and Win.",
        reply_markup=START_BTN
    )
    add_user(message.from_user.id, message.from_user.username)

# Import all handlers
import handlers.user
import handlers.admin
import handlers.game

if __name__ == "__main__":
    # For polling (default), PORT is not used. For webhooks, you can use it.
    app.run()


