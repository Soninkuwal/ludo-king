#from pyrogram import Client, filters
from bot import app
from pyrogram import filters
from pyrogram.types import Message
from database import save_screenshot, check_screenshot_utr, mark_win_verified, update_wallet



@app.on_message(filters.text & filters.group)
async def auto_table_create(client, message: Message):
    valid_amounts = [5,10,15,20,30,40,50]
    try:
        amount = int(message.text)
        if amount in valid_amounts:
            # Create new game table
            con = get_db()
            cur = con.cursor()
            cur.execute("INSERT INTO game_tables (group_id, amount) VALUES (?,?)", 
                       (message.chat.id, amount))
            table_id = cur.lastrowid
            con.commit()
            
            # Send table creation message
            await message.reply(
                f"New Ludo Table #{table_id} Created!\n"
                f"Stake: ₹{amount}\n"
                "Click JOIN to play!"
            )
    except ValueError:
        pass

@app.on_callback_query(filters.regex(r'^join_table_'))
async def handle_join_table(client, callback):
    table_id = int(callback.data.split('_')[-1])
    con = get_db()
    cur = con.cursor()
    
    cur.execute("SELECT players FROM game_tables WHERE id = ?", (table_id,))
    table = cur.fetchone()
    players = eval(table['players'])
    
    if callback.from_user.id not in players:
        players.append(callback.from_user.id)
        cur.execute("UPDATE game_tables SET players = ? WHERE id = ?",
                   (str(players), table_id))
        con.commit()
        
        await callback.answer("You've joined the table!")
        
        if len(players) == 2:
            await client.send_message(
                callback.message.chat.id,
                f"🚀 Game starting! Players: {', '.join([str(p) for p in players])}"
            )


#@app.on_message(filters.group & filters.photo)
#async def screenshot_upload_handler(client, message: Message):
#    user_id = message.from_user.id
#    if message.caption and "/win" in message.caption:
#        file_id = message.photo.file_id
#        save_screenshot(user_id, file_id)
#        await message.reply("Screenshot received! Admin will verify your win soon.")

#@app.on_message(filters.command("verifyutr"))
#async def verifyutr_handler(client, message: Message):
#    parts = message.text.split()
#    if len(parts) < 3:
#        await message.reply("Usage: /verifyutr <user_id> <utr>")
#        return
#    user_id, utr = int(parts[1]), parts[2]
#    if check_screenshot_utr(user_id, utr):
#        mark_win_verified(user_id)
#        await message.reply("UTR and screenshot verified. Win amount will be added.")
#    else:

#        await message.reply("UTR or screenshot not valid.")


