from pyrogram import Client, filters
from pyrogram.types import Message
from database import update_wallet, set_table_charge, get_admin_wallet, get_all_users, approve_withdrawal
from utils import is_admin

def admin_only(func):
    async def wrapper(client, message):
        if not is_admin(message.from_user.id):
            await message.reply("Admins only.")
            return
        await func(client, message)
    return wrapper

@Client.on_message(filters.command("addwallet"))
@admin_only
async def admin_addwallet_handler(client, message: Message):
    try:
        _, user_id, amount = message.text.split()
        update_wallet(int(user_id), float(amount))
        await message.reply("Wallet updated successfully.")
    except:
        await message.reply("Usage: /addwallet <user_id> <amount>")

@Client.on_message(filters.command("tablecharge"))
@admin_only
async def tablecharge_handler(client, message: Message):
    try:
        _, amount = message.text.split()
        set_table_charge(float(amount))
        await message.reply(f"Table charge set to ₹{amount}")
    except:
        await message.reply("Usage: /tablecharge <amount>")

@Client.on_message(filters.command("approve"))
@admin_only
async def approve_withdrawal_handler(client, message: Message):
    try:
        _, user_id, amount = message.text.split()
        approve_withdrawal(int(user_id), float(amount))
        await message.reply("Withdrawal approved.")
    except:
        await message.reply("Usage: /approve <user_id> <amount>")

@Client.on_message(filters.command("win"))
@admin_only
async def win_handler(client, message: Message):
    try:
        _, user_id, amount = message.text.split()
        update_wallet(int(user_id), float(amount))
        await message.reply("Win amount added to user wallet.")
    except:
        await message.reply("Usage: /win <user_id> <amount>")

@Client.on_message(filters.command("totalusers"))
@admin_only
async def totalusers_handler(client, message: Message):
    users = get_all_users()
    text = "All Users & Balances:\n"
    for user in users:
        text += f"{user['username']} ({user['user_id']}): ₹{user['wallet']:.2f}\n"
    await message.reply(text)

@Client.on_message(filters.command("adminwallet"))
@admin_only
async def adminwallet_handler(client, message: Message):
    amt = get_admin_wallet()
    await message.reply(f"Admin wallet: ₹{amt:.2f}")