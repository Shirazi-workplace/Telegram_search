import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🟣 **کاربر عزیز {user.first_name}**\n\n"
        "🔍 این ربات مطالب جستجو شده را در کانال زیر منتشر می‌کد:\n"
        "👉 https://t.me/archive_bot_shirazi\n\n"
        "📌 **طراح**: شیرازی\n"
        "📞 09031701895\n"
        "📢 @shirazi_ai",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()  # فقط Polling ساده!
