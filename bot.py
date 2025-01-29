import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Foydalanuvchilar uchun holatni saqlovchi lug'at
user_states = {}

# Start komandasi funksiyasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_states[user.id] = 0  # Foydalanuvchining holatini noldan boshlaymiz
    keyboard = [[InlineKeyboardButton("Task 1", url="https://t.me/pocketfi_bot/Contest?startapp=Usmon5504_9593"),
                 InlineKeyboardButton("Task 2", url="https://t.me/+cMUZesdEu25hODZi")],
                [InlineKeyboardButton("Confirm✅", callback_data="confirm")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = "Complete tasks and send me code"
    await update.message.reply_text(message, reply_markup=reply_markup)

# Confirm tugmasi bosilganda ishlovchi funksiya
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    state = user_states.get(user_id, 0)

    if state == 0:
        message = "You have not completed the tasks❌"
        keyboard = [[InlineKeyboardButton("Task 1", url="https://t.me/pocketfi_bot/Contest?startapp=Usmon5504_9593"),
                     InlineKeyboardButton("Task 2", url="https://t.me/+cMUZesdEu25hODZi")],
                    [InlineKeyboardButton("Confirm✅", callback_data="confirm")]]
        user_states[user_id] += 1
    elif state == 1:
        message = "You have not completed Task 1❌"
        keyboard = [[InlineKeyboardButton("Task 1", url="https://t.me/pocketfi_bot/Contest?startapp=Usmon5504_9593")],
                    [InlineKeyboardButton("Confirm✅", callback_data="confirm")]]
        user_states[user_id] += 1
    else:
        user = query.from_user
        name = f"<a href='tg://settings'>{user.first_name} {user.last_name or ''}</a>"
        message = f"Hello {name}, send me code"
        keyboard = []  # Endi tugmalarni olib tashlaymiz
        user_states[user_id] = 3  # Endi bot odatdagidek ishlaydi
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await query.message.edit_text(message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    await query.answer()

# Foydalanuvchi xabariga javob berish funksiyasi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = user_states.get(user_id, 0)

    if state < 3:
        message = "You have not completed the tasks❌"
        keyboard = [[InlineKeyboardButton("Task 1", url="https://t.me/pocketfi_bot/Contest?startapp=Usmon5504_9593"),
                     InlineKeyboardButton("Task 2", url="https://t.me/+cMUZesdEu25hODZi")],
                    [InlineKeyboardButton("Confirm✅", callback_data="confirm")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        text = update.message.text

        # Agar foydalanuvchi 1 dan 500 gacha raqam yuborsa
        if text.isdigit() and 1 <= int(text) <= 500:
            number = text  # Foydalanuvchi yuborgan raqamni oladi
            keyboard = [[InlineKeyboardButton(f"Watch video {number}", url="https://t.me/+K0HW9J-U5IoxMGMy")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Click the button to watch👇", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Wrong code")

# Asosiy ishga tushirish qismi
def main():
    # Bot tokenini kiritish
    TOKEN = "7639778320:AAEhVyjBcjzrRjUXYPLCadGC1Ma6_vmAd_M"

    application = Application.builder().token(TOKEN).build()

    # Start komandasi uchun handler qo'shish
    application.add_handler(CommandHandler("start", start))
    
    # Callback query uchun handler qo'shish
    application.add_handler(CallbackQueryHandler(confirm, pattern="confirm"))

    # Xabarlar uchun handler qo'shish
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    asyncio.run(application.run_polling())

if __name__ == "__main__":
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
