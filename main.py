import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
from datetime import datetime

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# متن نمایشی قبل از استارت
PRE_START_MESSAGE = """
🟢 <b>کاربر عزیز</b> <code>{user_name}</code> 👋

📌 این ربات مطالب جستجو شده را در کانال زیر با ذکر منبع منتشر می‌کند:
🔗 <a href="https://t.me/archive_bot_shirazi">کانال آرشیو مطالب</a>

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
✨ <b>برای شروع دکمه استارت را بزنید</b> ✨
"""

# متن صفحه اصلی
WELCOME_MESSAGE = """
🎉 <b>به ربات جستجوگر پیشرفته خوش آمدید!</b>

🔍 <i>امکانات ربات:</i>
• جستجوی هوشمند در منابع
• آرشیو خودکار مطالب
• ذخیره‌سازی ابری

🛠 <b>طراحی و توسعه:</b>
👤 <code>شیرازی</code>
📞 <code>09031701895</code>
📢 @shirazi_ai

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""

# دکمه‌های صفحه اصلی
keyboard = [
    [InlineKeyboardButton("🚀 شروع جستجو", callback_data='search')],
    [InlineKeyboardButton("📚 آرشیو من", callback_data='archive')],
    [InlineKeyboardButton("⚙️ تنظیمات پیشرفته", callback_data='settings')],
    [InlineKeyboardButton("📣 کانال آرشیو", url='https://t.me/archive_bot_shirazi')]
]

async def pre_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler برای پیام اولیه قبل از استارت"""
    user = update.effective_user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=PRE_START_MESSAGE.format(user_name=user.first_name or "کاربر"),
        parse_mode='HTML',
        disable_web_page_preview=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler برای دستور /start"""
    user = update.effective_user
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # انیمیشن تایپ کردن
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # ارسال پیام خوش‌آمدگویی با طراحی حرفه‌ای
    await update.message.reply_text(
        text=f"👋 <b>سلام {user.mention_markdown_v2()}</b>\n" + WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler برای دکمه‌های اینلاین"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'search':
        await query.edit_message_text(
            text="🔍 <b>حالت جستجوی پیشرفته</b>\n\nلطفا عبارت مورد نظر خود را وارد کنید:",
            parse_mode='HTML'
        )
    else:
        await query.edit_message_text(
            text="⚡ <b>این بخش به زودی فعال خواهد شد</b>\n\n@shirazi_ai",
            parse_mode='HTML'
        )

def main():
    """اجرای اصلی ربات"""
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    # اضافه کردن handlerها
    application.add_handler(MessageHandler(filters.ALL, pre_start), group=0)
    application.add_handler(CommandHandler('start', start), group=1)
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # اجرای ربات
    application.run_polling()

if __name__ == '__main__':
    main()
