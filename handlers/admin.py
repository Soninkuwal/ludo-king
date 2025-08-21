from bot import app
from pyrogram import filters
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


@app.on_message(filters.command("verifyutr"))
@admin_only
async def verify_utr_handler(client, message: Message):
    try:
        _, utr = message.text.split()
        con = get_db()
        cur = con.cursor()
        cur.execute("UPDATE screenshots SET status='verified' WHERE utr=?", (utr,))
        con.commit()
        await message.reply(f"UTR {utr} verified successfully")
    except:
        await message.reply("Usage: /verifyutr <utr_number>")
        

#@app.on_message(filters.command("addwallet"))
#@admin_only
#async def admin_addwallet_handler(client, message: Message):
#    try:
#        _, user_id, amount = message.text.split()
#        update_wallet(int(user_id), float(amount))
#        await message.reply("Wallet updated successfully.")
#    except:
#        await message.reply("Usage: /addwallet <user_id> <amount>")

@app.on_message(filters.command("addwallet"))
@admin_only 
async def admin_addwallet_handler(client, message: Message):
    try:
        _, user_id, amount = message.text.split()
        update_wallet(int(user_id), float(amount))
        await message.reply(f"💳 Wallet updated for user {user_id}")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")



@app.on_message(filters.command("tablecharge"))
@admin_only
async def tablecharge_handler(client, message: Message):
    try:
        _, amount = message.text.split()
        set_table_charge(float(amount))
        await message.reply(f"Table charge set to ₹{amount}")
    except:
        await message.reply("Usage: /tablecharge <amount>")


@app.on_message(filters.command("approve"))
@admin_only
async def approve_withdrawal_handler(client, message: Message):
    try:
        _, user_id, amount = message.text.split()
        if approve_withdrawal(int(user_id), float(amount)):
            await message.reply(f"✅ Approved ₹{amount} withdrawal for user {user_id}")
        else:
            await message.reply("❌ No pending withdrawal found")
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")

@app.on_message(filters.command("totalusers"))
@admin_only
async def totalusers_handler(client, message: Message):
    users = get_all_users()
    count = len(users)
    total = sum(u['wallet'] for u in users)
    await message.reply(
        f"👥 Total Users: {count}\n"
        f"💰 Total Wallet Balance: ₹{total:.2f}"
    )



#@app.on_message(filters.command("approve"))
#@admin_only
#async def approve_withdrawal_handler(client, message: Message):
#    try:
#        _, user_id, amount = message.text.split()
#        approve_withdrawal(int(user_id), float(amount))
#        await message.reply("Withdrawal approved.")
#    except:
#        await message.reply("Usage: /approve <user_id> <amount>")

#@app.on_message(filters.command("win"))
#@admin_only
#async def win_handler(client, message: Message):
#    try:
#        _, user_id, amount = message.text.split()
#        update_wallet(int(user_id), float(amount))
#        await message.reply("Win amount added to user wallet.")
#    except:
#        await message.reply("Usage: /win <user_id> <amount>")


@app.on_message(filters.command("win"))
@admin_only
async def win_handler(client, message: Message):
    try:
        _, user_id, amount = message.text.split()
        if not user_id.isdigit():
            raise ValueError
        update_wallet(int(user_id), float(amount))
        await message.reply(f"✅ Successfully added ₹{amount} to user {user_id}'s wallet")
    except:
        await message.reply("⚠️ Usage: /win <user_id> <amount>")





#@app.on_message(filters.command("totalusers"))
#@admin_only
#async def totalusers_handler(client, message: Message):
#    users = get_all_users()
#    text = "All Users & Balances:\n"
#    for user in users:
#        text += f"{user['username']} ({user['user_id']}): ₹{user['wallet']:.2f}\n"
#    await message.reply(text)

#@app.on_message(filters.command("adminwallet"))
#@admin_only
#async def adminwallet_handler(client, message: Message):
#    amt = get_admin_wallet()

#    await message.reply(f"Admin wallet: ₹{amt:.2f}")

@app.on_message(filters.command("adminwallet"))
@admin_only
async def adminwallet_handler(client, message: Message):
    amt = get_admin_wallet()
    await message.reply(
        f"🏦 Admin Wallet Balance:\n"
        f"💵 ₹{amt:.2f}\n\n"
        "Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    


# Command: /addgroup <group_id>
@app.on_message(filters.command("addgroup")) # & filters.user(ADMINS)
async def add_premium_group(client, message):
    try:
        group_id = int(message.command[1])
        database.add_premium_group(group_id)
        await message.reply(f"🆕 Group {group_id} added successfully!")
    except:
        await message.reply("❌ Invalid format. Use /addgroup group_id")


@app.on_message(filters.command("addplan"))
@admin_only
async def add_plan_handler(client, message: Message):
    try:
        _, plan_name, duration, price = message.text.split()
        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO plans (plan_name, duration_days, price) VALUES (?,?,?)",
                   (plan_name, int(duration), float(price)))
        con.commit()
        await message.reply(f"Plan {plan_name} added successfully")
    except:
        await message.reply("Usage: /addplan <name> <duration_days> <price>")



@app.on_message(filters.command("setplan"))
async def set_subscription_plan(client, message):
    plans = {
        "1mon": (100, 30),
        "3mon": (300, 90),
        "12mon": (1200, 365)
    }
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


@app.on_message(filters.command("groupinfo") & filters.user(ADMINS))
async def groupinfo_handler(client, message: Message):
    try:
        group_id = int(message.command[1])
        group = get_group(group_id)
        await message.reply(
            f"📊 Group {group_id} Info:\n"
            f"Premium: {group['is_premium'] and '✅' or '❌'}\n"
            f"Plan: {group['plan_name'] or 'None'}\n"
            f"Members: {get_group_member_count(group_id)}"
        )
    except:
        await message.reply("Usage: /groupinfo <group_id>")


# Command: /groupinfo <group_id>
#@app.on_message(filters.command("groupinfo"))
#async def groupinfo_handler(client, message):
#    if message.from_user.id != OWNER_ID:
#        return await message.reply("Only owner can check group info.")
#    parts = message.text.split()
#    if len(parts) < 2:
#        return await message.reply("Usage: /groupinfo <group_id>")
#    group = get_group(int(parts[1]))
#    if not group:
#        return await message.reply("Group not found.")
#    await message.reply(
#        f"Group: {group['group_id']}\nPremium: {group['is_premium']}\n"
#        f"Plan: {group['plan_start']} to {group['plan_end']}\n"
#        f"Added by: {group['added_by']}"
#    )


