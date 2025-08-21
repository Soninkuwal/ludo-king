from pyrogram import Client, filters
from pyrogram.types import Message
from database import update_wallet, set_table_charge, get_admin_wallet, get_all_users, approve_withdrawal
from utils import is_admin
from datetime import datetime, timedelta
from database import add_group, set_group_premium, get_plan, get_group
from config import OWNER_ID, ADMINS

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


# Command: /addgroup <group_id>
@Client.on_message(filters.command("addgroup"))
async def addgroup_handler(client, message):
    if message.from_user.id not in ADMINS and message.from_user.id != OWNER_ID:
        return await message.reply("Only owner/admin can approve groups.")
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: /addgroup <group_id>")
    group_id = int(parts[1])
    add_group(group_id, message.from_user.id)
    await message.reply(f"Group {group_id} approved! Now add premium plan if needed.")

# Command: /addplan <group_id> <plan_name>
@Client.on_message(filters.command("addplan"))
async def addplan_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only owner can assign premium plans.")
    parts = message.text.split()
    if len(parts) < 3:
        return await message.reply("Usage: /addplan <group_id> <plan_name>")
    group_id = int(parts[1])
    plan_name = parts[2]
    plan = get_plan(plan_name)
    if not plan:
        return await message.reply("Plan not found. Use 1mon/3mon/12mon.")
    start = datetime.utcnow()
    end = start + timedelta(days=plan['duration_days'])
    set_group_premium(group_id, 1, start.isoformat(), end.isoformat())
    await message.reply(f"Group {group_id} upgraded to premium until {end.date()}.")

# Command: /groupinfo <group_id>
@Client.on_message(filters.command("groupinfo"))
async def groupinfo_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Only owner can check group info.")
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: /groupinfo <group_id>")
    group = get_group(int(parts[1]))
    if not group:
        return await message.reply("Group not found.")
    await message.reply(
        f"Group: {group['group_id']}\nPremium: {group['is_premium']}\n"
        f"Plan: {group['plan_start']} to {group['plan_end']}\n"
        f"Added by: {group['added_by']}"
    )
