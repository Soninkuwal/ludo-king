# Ludo King Telegram Bot

A Telegram bot for playing Ludo King in groups with wallet, admin panel, verification & payout system.

## Features

- Group Ludo table creation
- Join via link
- Wallet for users and admins
- Screenshot win verification
- Admins approve payments, edit table charge & more
- Multiple admins/groups supported
- Withdrawals, wallet check, group admin earnings & more!

## Setup

### 1. Create a Telegram Bot

- [@BotFather](https://t.me/BotFather) se bot banao. API Token le lo.

### 2. Get Telegram API ID & Hash

- [https://my.telegram.org](https://my.telegram.org) pe login karo aur API ID & API Hash le lo.

### 3. Clone Repo & Install

```bash
git clone https://github.com/yourusername/ludo_king_telegram_bot.git
cd ludo_king_telegram_bot
pip install -r requirements.txt
```

### 4. Add Config

Edit `config.py` with your API ID, hash, bot token, and admin IDs.

### 5. Run Bot

```bash
python bot.py
```

---

## Deploy on Koyeb, Render, Heroku, Cloudflare

### Koyeb

- [Koyeb Python Deploy Guide](https://koyeb.com/docs/platform/deploy-applications/python)

### Render

- [Render Python App Guide](https://render.com/docs/deploy-python)

### Heroku

```bash
heroku create
heroku buildpacks:add heroku/python
git push heroku main
heroku config:set API_ID=xxx API_HASH=xxx BOT_TOKEN=xxx
heroku ps:scale web=1
```

## Deploy on Koyeb, Render, Heroku

### Port Variable

On Koyeb, Render, and Heroku, the `PORT` environment variable is automatically set by the platform.  
This bot is ready for polling mode (no special port required), but if you use webhooks or need port, the following will work:

- The bot reads `PORT` from environment (defaults to 8080).
- For Heroku: No extra changes needed, just ensure your Procfile exists and deploy.

### Heroku

```bash
heroku create
heroku buildpacks:add heroku/python
git push heroku main
heroku config:set API_ID=xxx API_HASH=xxx BOT_TOKEN=xxx
```

### Cloudflare (via Workers for API or with worker-proxy)

- [Cloudflare Workers Python Guide](https://developers.cloudflare.com/workers/)

---


## Health Checks

- Your instance will pass health checks if `/health` returns `OK` (HTTP 200).
- The bot will reply to `/start` commands in private and groups.
- To test: Open `https://your-app-url/health` in a browser, and use `/start` in Telegram with your bot.

- 

## Commands

- `/start` - Start bot, join table links
- `/wallet` - Check wallet
- `/withdraw <amount>` - Withdraw request (admin approve)
- `/addwallet <user_id> <amt>` - (Admin) add wallet
- `/tablecharge <amt>` - (Admin) edit table charge
- `/adminwallet` - (Admin) check admin wallet
- `/totalusers` - (Admin) get all users & balances
- `/win <user_id> <amt>` - (Admin) add win amount after screenshot verified

---

## How It Works

- Group me add karo
- Do user amount send kare, unhe join/chat links milti hai
- Game ke baad winner screenshot upload kare, admin verify kare
- Amount auto update ho wallet me
- User withdraw request kare, admin approve kare

---

## Notes

- Multiple admins/groups support
- User, admin, and game data stored in SQLite
- Easily extensible for new features

---

## License


MIT

