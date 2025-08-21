from pyrogram import Client, filters
from pyrogram.types import Message
from database import add_user, get_wallet, update_wallet, add_withdrawal, get_username
from database import get_group
from datetime import datetime
from config import OWNER_ID


def is_group_allowed(group_id):
    group = get_group(group_id)
    if not group:
        return False
    # Owner's group always allowed
    if group['added_by'] == OWNER_ID:
        return True
    # Premium check
    if group['is_premium']:
        if group['plan_end'] and datetime.fromisoformat(group['plan_end']) > datetime.utcnow():
            return True
    return False

@Client.on_message(filters.group & filters.text & filters.regex(r"^\d+$"))
async def amount_message_handler(client, message):
    group_id = message.chat.id
    if not is_group_allowed(group_id):
        await message.reply(
            "This group is not premium or not approved.\n"
            "Contact bot owner to activate premium plan.\n"
            f"Owner: [{OWNER_ID}](tg://user?id={OWNER_ID})",
            parse_mode="markdown"
        )
        return
    # ... rest of logic for table creation ...



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
