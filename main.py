import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import os
from datetime import datetime

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# متن صفحه اصلی با طراحی زیبا
WELCOME_MESSAGE = """
✨ <b>به ربات جستجوگر و آرشیو تلگرام خوش آمدید</b> ✨

<i>راهنمای هوشمند برای جستجوی پیشرفته در تلگرام</i>

🛠 <b>طراح و برنامه‌نویس</b>: شیرازی
📞 <code>09031701895</code>
📢 @shirazi_ai

▬▬▬▬▬▬▬▬▬▬▬▬
"""

# دکمه‌های صفحه اصلی
keyboard = [
    [InlineKeyboardButton("🔍 جستجوی پیشرفته", callback_data='search')],
    [InlineKeyboardButton("📁 آرشیو من", callback_data='archive')],
    [InlineKeyboardButton("⚙️ تنظیمات", callback_data='settings')],
    [InlineKeyboardButton("📞 پشتیبانی", url='https://t.me/shirazi_ai')]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler برای دستور /start"""
    user = update.effective_user
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ارسال پیام خوش‌آمدگویی با انیمیشن تایپ کردن
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(
        text=f"سلام {user.mention_markdown_v2()} 👋\n" + WELCOME_MESSAGE,
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
            text="🔍 <b>حالت جستجوی پیشرفته فعال شد</b>\n\nلطفا عبارت مورد نظر خود را ارسال کنید:",
            parse_mode='HTML'
        )
    elif query.data == 'archive':
        await query.edit_message_text(
            text="📁 <b>آرشیو شخصی شما</b>\n\nدر حال حاضر آرشیوی وجود ندارد.",
            parse_mode='HTML'
        )
    else:
        await query.edit_message_text(
            text="⚙️ <b>تنظیمات ربات</b>\n\nاین بخش به زودی اضافه خواهد شد.",
            parse_mode='HTML'
        )

def main():
    """اجرای اصلی ربات"""
    # ایجاد اپلیکیشن با توکن ربات
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    # اضافه کردن handlerها
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # اجرای ربات در حالت polling (برای تست)
    application.run_polling()

if __name__ == '__main__':
    main()
