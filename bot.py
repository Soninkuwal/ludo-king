from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from database import create_tables, add_user

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

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    thumb = "start_thumb.jpg"
    await message.reply_photo(
        thumb,
        caption="Welcome to Ludo King Bot! Play and Win.\nJoin a match, send /wallet to check balance.",
        reply_markup=START_BTN
    )
    add_user(message.from_user.id, message.from_user.username)

# Import all handlers
import handlers.user
import handlers.admin
import handlers.game

app.run()