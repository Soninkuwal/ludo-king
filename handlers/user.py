from pyrogram import Client, filters
from pyrogram.types import Message
from database import add_user, get_wallet, update_wallet, add_withdrawal, get_username

@Client.on_message(filters.command("wallet"))
async def wallet_handler(client, message: Message):
    user_id = message.from_user.id
    balance = get_wallet(user_id)
    await message.reply(f"Your wallet balance: ₹{balance:.2f}")

@Client.on_message(filters.command("withdraw"))
async def withdraw_handler(client, message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("Usage: /withdraw <amount>")
        return
    amount = float(parts[1])
    user_id = message.from_user.id
    balance = get_wallet(user_id)
    if amount > balance:
        await message.reply("Insufficient balance.")
        return
    add_withdrawal(user_id, amount)
    await message.reply(
        "Withdrawal request submitted. Please send your payment details to the admin."
    )

@Client.on_callback_query(filters.regex("join_table"))
async def join_table_handler(client, callback_query):
    # For demo: Just reply, actual logic needed
    await callback_query.answer("You have joined the Ludo table. Wait for another player.")

@Client.on_message(filters.command("tablechat"))
async def tablechat_handler(client, message: Message):
    # Demo: just for sample
    await message.reply("Chat link functionality is under development.")