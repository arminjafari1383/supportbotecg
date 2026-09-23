# 🤖 Eco Smart Support Bot

A bilingual (Persian/English) Telegram support bot for the **Eco Smart** mini-app ecosystem.

## ✨ Features

- 🌐 **Bilingual** — auto-detects Persian/English
- 📋 **FAQ system** — 6 main topics with inline buttons
- 🎫 **Ticket system** — users send questions, admin replies via `/reply`
- 💬 **Inline keyboards** — clean Telegram-native UX
- 📊 **Persistent storage** — tickets saved to JSON

## 🚀 Quick Start

### 1. Create your bot
- Talk to [@BotFather](https://t.me/BotFather) on Telegram
- Send `/newbot`, follow prompts, copy the **token**

### 2. Get your chat ID
- Talk to [@userinfobot](https://t.me/userinfobot)
- It will reply with your numeric **chat ID**

### 3. Deploy on Railway (recommended, free)

1. Push this folder to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variables:
   - `BOT_TOKEN` = your bot token
   - `ADMIN_CHAT_ID` = your chat id
4. Railway auto-detects Python and deploys

### 4. Deploy on Render (alternative)

1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Build command: `pip install -r requirements.txt`
4. Start command: `python bot.py`
5. Add env vars in dashboard

### 5. Run locally

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then edit .env
python bot.py
```

## 📖 Usage

### For users
- Send `/start` → see menu
- Tap a topic → see FAQ in both languages
- Tap "Send ticket" → write question → admin gets notified

### For admin (you)
- Receive ticket notification in your private chat
- Reply with: `/reply T-0001 your message here`
- User receives your reply in their chat

## 🗂 Project structure

```
eco-smart-bot/
├── bot.py              # Main bot logic
├── requirements.txt    # Python deps
├── Procfile            # Railway/Render config
├── runtime.txt         # Python version
├── .env.example        # Env var template
├── .gitignore
└── README.md
```

## 🛠 Customization

### Add a new FAQ topic
Edit the `FAQ` dict in `bot.py`:

```python
FAQ["new_topic"] = {
    "fa": "پاسخ فارسی...",
    "en": "English answer...",
}
```

Then add a button in `main_menu_keyboard()`.

### Change ticket storage
Replace `tickets.json` with a database (SQLite, Postgres) for production scale.

## 📜 License

MIT — free to use, modify, distribute.
