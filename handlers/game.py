#from pyrogram import Client, filters
from bot import app
from pyrogram.types import Message
from database import save_screenshot, check_screenshot_utr, mark_win_verified, update_wallet

@app.on_message(filters.group & filters.photo)
async def screenshot_upload_handler(client, message: Message):
    user_id = message.from_user.id
    if message.caption and "/win" in message.caption:
        file_id = message.photo.file_id
        save_screenshot(user_id, file_id)
        await message.reply("Screenshot received! Admin will verify your win soon.")

@app.on_message(filters.command("verifyutr"))
async def verifyutr_handler(client, message: Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.reply("Usage: /verifyutr <user_id> <utr>")
        return
    user_id, utr = int(parts[1]), parts[2]
    if check_screenshot_utr(user_id, utr):
        mark_win_verified(user_id)
        await message.reply("UTR and screenshot verified. Win amount will be added.")
    else:

        await message.reply("UTR or screenshot not valid.")
