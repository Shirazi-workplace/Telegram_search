import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('TELEGRAM_TOKEN')
PORT = int(os.environ.get('PORT', 10000))

# متن پیش‌نمایش قبل از استارت
PRE_START_MESSAGE = """
🟣 <b>کاربر عزیز {user_name} عزیز</b> 🟣

📚 این ربات مطالب جستجو شده را در کانال زیر منتشر می‌کند:
👉 <a href="https://t.me/archive_bot_shirazi">کانال آرشیو مطالب</a>

✨ <b>برای شروع دکمه /start را بزنید</b> ✨
"""

# متن صفحه اصلی
START_MESSAGE = """
🎯 <b>ربات جستجوی حرفه‌ای فعال شد!</b>

🔍 امکانات ربات:
• جستجوی هوشمند در منابع
• آرشیو خودکار مطالب
• ذخیره‌سازی ابری

📌 <i>طراحی شده توسط شیرازی</i>
📞 <code>09031701895</code>
"""

async def pre_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام قبل از شروع"""
    if update.message and not update.message.text.startswith('/'):
        user = update.effective_user
        await update.message.reply_text(
            text=PRE_START_MESSAGE.format(user_name=user.first_name),
            parse_mode='HTML',
            disable_web_page_preview=True
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور استارت"""
    keyboard = [
        [InlineKeyboardButton("🔍 شروع جستجو", callback_data='search')],
        [InlineKeyboardButton("📌 کانال آرشیو", url='https://t.me/archive_bot_shirazi')]
    ]
    
    await update.message.reply_text(
        text=START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pre_start))
    
    # تنظیمات اجرا
    if os.getenv('RENDER'):
        app.run_webhook(
            listen='0.0.0.0',
            port=PORT,
            url_path=TOKEN,
            webhook_url=f'https://your-bot-name.onrender.com/{TOKEN}'
        )
    else:
        app.run_polling()

if __name__ == '__main__':
    main()
