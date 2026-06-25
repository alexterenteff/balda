import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- ТОКЕН ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден!")
    exit(1)

# --- ХРАНИЛИЩЕ (баланс в памяти) ---
user_balances = {}

# --- КОМАНДА /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Если новый пользователь — ставим баланс 0
    if user_id not in user_balances:
        user_balances[user_id] = 0

    # Кнопка "Пинать Балду"
    keyboard = [[InlineKeyboardButton("👊 Пинать Балду", callback_data="punch")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Текст приветствия
    text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я Балда. Пни меня, чтобы зарабатывать деньги.\n\n"
        f"💰 Твой баланс: {user_balances[user_id]} руб."
    )

    await update.message.reply_text(text, reply_markup=reply_markup)

# --- КОГДА НАЖАЛИ КНОПКУ ---
async def punch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Если пользователя нет — добавляем
    if user_id not in user_balances:
        user_balances[user_id] = 0

    # Прибавляем 100 рублей
    user_balances[user_id] += 100

    # Кнопка остаётся
    keyboard = [[InlineKeyboardButton("👊 Пинать Балду ещё раз", callback_data="punch")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Обновляем сообщение
    text = (
        f"💥 БАЦ! Ты пнул Балду!\n"
        f"💰 Заработано: +100 руб.\n\n"
        f"Твой баланс: {user_balances[user_id]} руб."
    )

    await query.edit_message_text(text, reply_markup=reply_markup)

# --- ЗАПУСК ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(punch, pattern="punch"))

    print("✅ Бот Балда запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
