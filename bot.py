import health
"""
Eco Smart Support Bot
ربات پشتیبانی اکو اسمارت
A bilingual (Persian/English) Telegram support bot for the Eco Smart mini-app.
"""

import os
import json
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "0"))  # your personal chat id
DATA_FILE = "tickets.json"

# ─────────────────────────────────────────────────────────────
# FAQ DATABASE (bilingual)
# ─────────────────────────────────────────────────────────────
FAQ = {
    "claim": {
        "fa": "🎁 **کلایم رایگان EPL**\n\nهر ساعت یکبار میتونید از طریق مینی‌اپ EPL رایگان کلایم کنید.\n\n⏰ محدودیت زمانی: هر ۶۰ دقیقه\n💰 مقدار: بسته به سطح شما متفاوته",
        "en": "🎁 **Free EPL Claim**\n\nYou can claim free EPL every hour through the mini-app.\n\n⏰ Cooldown: every 60 minutes\n💰 Amount: varies by your level",
    },
    "referral": {
        "fa": "👥 **سیستم معرفی**\n\n• معرفی مستقیم (سطح 1): **1000 EPL**\n• سطوح 2 تا 8: هر کدوم **500 EPL**\n\n💡 هرچه بیشتر معرفی کنید، درآمد بیشتری دارید!",
        "en": "👥 **Referral System**\n\n• Direct referral (Level 1): **1000 EPL**\n• Levels 2-8: **500 EPL** each\n\n💡 The more you refer, the more you earn!",
    },
    "staking": {
        "fa": "💰 **استیکینگ**\n\n• مدت: **365 روز**\n• سود ماهانه: **5%**\n• پرداخت سود: **USDT یا ECG**\n\n📌 پاداش معرف:\n• سطح 1: **5%** لحظه‌ای\n• سطوح 2-8: **1%**",
        "en": "💰 **Staking**\n\n• Duration: **365 days**\n• Monthly yield: **5%**\n• Payout: **USDT or ECG**\n\n📌 Referral rewards:\n• Level 1: **5%** instant\n• Levels 2-8: **1%**",
    },
    "withdraw": {
        "fa": "💸 **برداشت**\n\n• پاداش‌های USDT/ECG: **لحظه‌ای**\n• سود استیک: بعد از **1 ماه** قابل برداشت\n\n⚠️ ابتدا باید ولت رو کانکت کنید",
        "en": "💸 **Withdrawal**\n\n• USDT/ECG rewards: **instant**\n• Staking yield: available after **1 month**\n\n⚠️ You must connect your wallet first",
    },
    "payment": {
        "fa": "💳 **پرداخت**\n\n• خرید ارز: با **TON**\n• برداشت پاداش: **TON یا ECG**\n\n🔐 پرداخت‌ها از طریق ولت متصل شده انجام میشه",
        "en": "💳 **Payment**\n\n• Buy currency: with **TON**\n• Withdraw rewards: **TON or ECG**\n\n🔐 Payments are processed through your connected wallet",
    },
    "vpn": {
        "fa": "🌐 **VPN رایگان**\n\nبعد از معرفی **5 نفر**، گزینه VPN رایگان برات باز میشه.\n\n✅ پیشرفت شما رو تو مینی‌اپ ببین",
        "en": "🌐 **Free VPN**\n\nAfter referring **5 people**, the free VPN option unlocks for you.\n\n✅ Check your progress in the mini-app",
    },
}

# ─────────────────────────────────────────────────────────────
# TICKET STORAGE
# ─────────────────────────────────────────────────────────────
def load_tickets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_tickets(tickets):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────────────────────────
# LANGUAGE DETECTION (simple)
# ─────────────────────────────────────────────────────────────
def detect_lang(text: str) -> str:
    persian_chars = set("ابپتثجچحخدذرزسشصضطظعغفقکگلمنوهی")
    return "fa" if any(c in persian_chars for c in text) else "en"

# ─────────────────────────────────────────────────────────────
# KEYBOARDS
# ─────────────────────────────────────────────────────────────
def main_menu_keyboard(lang="en"):
    if lang == "fa":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🎁 کلایم EPL", callback_data="faq_claim"),
             InlineKeyboardButton("👥 معرفی", callback_data="faq_referral")],
            [InlineKeyboardButton("💰 استیکینگ", callback_data="faq_staking"),
             InlineKeyboardButton("💸 برداشت", callback_data="faq_withdraw")],
            [InlineKeyboardButton("💳 پرداخت", callback_data="faq_payment"),
             InlineKeyboardButton("🌐 VPN", callback_data="faq_vpn")],
            [InlineKeyboardButton("📩 ارسال تیکت به ادمین", callback_data="new_ticket")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 EPL Claim", callback_data="faq_claim"),
         InlineKeyboardButton("👥 Referral", callback_data="faq_referral")],
        [InlineKeyboardButton("💰 Staking", callback_data="faq_staking"),
         InlineKeyboardButton("💸 Withdraw", callback_data="faq_withdraw")],
        [InlineKeyboardButton("💳 Payment", callback_data="faq_payment"),
         InlineKeyboardButton("🌐 VPN", callback_data="faq_vpn")],
        [InlineKeyboardButton("📩 Send ticket to admin", callback_data="new_ticket")],
        [InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")],
    ])

# ─────────────────────────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = detect_lang(update.message.text or "")
    if lang == "fa":
        msg = "👋 سلام! به پشتیبانی اکو اسمارت خوش اومدی.\n\nیه موضوع رو انتخاب کن یا تیکت بفرست:"
    else:
        msg = "👋 Welcome to Eco Smart support!\n\nPick a topic or send a ticket:"
    await update.message.reply_text(msg, reply_markup=main_menu_keyboard(lang))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Language switch
    if data == "lang_fa":
        await query.edit_message_text("یه موضوع انتخاب کن:", reply_markup=main_menu_keyboard("fa"))
        return
    if data == "lang_en":
        await query.edit_message_text("Pick a topic:", reply_markup=main_menu_keyboard("en"))
        return

    # FAQ buttons
    if data.startswith("faq_"):
        key = data.replace("faq_", "")
        if key in FAQ:
            # Show both languages
            text = FAQ[key]["fa"] + "\n\n──────────────\n\n" + FAQ[key]["en"]
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back / بازگشت", callback_data="back_main")]])
            await query.edit_message_text(text, reply_markup=kb)
        return

    # Back to main
    if data == "back_main":
        await query.edit_message_text(
            "Pick a topic / یه موضوع انتخاب کن:",
            reply_markup=main_menu_keyboard("en")
        )
        return

    # New ticket
    if data == "new_ticket":
        context.user_data["awaiting_ticket"] = True
        if detect_lang(query.message.text or "") == "fa":
            await query.edit_message_text(
                "📝 سوالت رو بنویس. ادمین به زودی جواب میده.\n\n❌ برای لغو /cancel رو بزن."
            )
        else:
            await query.edit_message_text(
                "📝 Write your question. An admin will reply soon.\n\n❌ Send /cancel to abort."
            )
        return

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_ticket"):
        await update.message.reply_text(
            "Use /start to open the menu.\nاز /start برای منو استفاده کن."
        )
        return

    # Save ticket
    tickets = load_tickets()
    ticket_id = f"T-{len(tickets)+1:04d}"
    user = update.effective_user
    tickets[ticket_id] = {
        "user_id": user.id,
        "username": user.username or user.first_name,
        "message": update.message.text,
        "time": datetime.now().isoformat(),
        "status": "open",
    }
    save_tickets(tickets)
    context.user_data["awaiting_ticket"] = False

    # Confirm to user
    lang = detect_lang(update.message.text)
    if lang == "fa":
        await update.message.reply_text(
            f"✅ تیکت ثبت شد!\n\n🆔 کد تیکت: `{ticket_id}`\n⏱ ادمین به زودی جواب میده.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            f"✅ Ticket received!\n\n🆔 Ticket ID: `{ticket_id}`\n⏱ Admin will reply soon.",
            parse_mode="Markdown"
        )

    # Notify admin
    if ADMIN_CHAT_ID:
        admin_msg = (
            f"🆕 **New Ticket** `{ticket_id}`\n\n"
            f"👤 User: @{user.username or '—'} (id: `{user.id}`)\n"
            f"💬 Message:\n{update.message.text}\n\n"
            f"↩️ Reply with: `/reply {ticket_id} your message`"
        )
        await context.bot.send_message(ADMIN_CHAT_ID, admin_msg, parse_mode="Markdown")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_ticket"] = False
    await update.message.reply_text("❌ Cancelled. /start to return.")

async def reply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin only: reply to a ticket."""
    if update.effective_user.id != ADMIN_CHAT_ID:
        return
    try:
        ticket_id = context.args[0]
        reply_text = " ".join(context.args[1:])
        tickets = load_tickets()
        if ticket_id not in tickets:
            await update.message.reply_text("❌ Ticket not found.")
            return
        user_id = tickets[ticket_id]["user_id"]
        await context.bot.send_message(
            user_id,
            f"💬 **Support reply / پاسخ پشتیبانی**\n\n{reply_text}\n\n🆔 `{ticket_id}`",
            parse_mode="Markdown"
        )
        tickets[ticket_id]["status"] = "answered"
        save_tickets(tickets)
        await update.message.reply_text(f"✅ Reply sent to {ticket_id}")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /reply T-0001 your message")

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("reply", reply_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🤖 Eco Smart Support Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
