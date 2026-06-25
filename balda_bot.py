import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- ТОКЕН ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден!")
    exit(1)

# --- КОМАНДА /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name

    # Кнопка "Пинать Балду"
    keyboard = [[InlineKeyboardButton("👊 Пинать Балду", callback_data="punch")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"Привет, {name}! 👋\nЯ Балда, пни меня, чтобы зарабатывать деньги."

    await update.message.reply_text(text, reply_markup=reply_markup)

# --- КОГДА НАЖАЛИ "Пинать Балду" ---
async def punch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Кнопка "Подробнее"
    keyboard = [[InlineKeyboardButton("📖 Подробнее", callback_data="more")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "💰 Заработок на курьерах"

    await query.edit_message_text(text, reply_markup=reply_markup)

# --- КОГДА НАЖАЛИ "Подробнее" ---
async def more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Убираем кнопки, оставляем только текст
    text = (
        "🚚 *Заработок на курьерах*\n\n"
        "Ты можешь зарабатывать деньги, работая курьером в сервисах доставки.\n"
        "Регистрируйся в Яндекс Еде, Ozon, Delivery Club и получай деньги за заказы.\n\n"
        "Балда поможет тебе с регистрацией и даст промты для контента.\n\n"
        "Напиши /start, чтобы вернуться в меню."
    )

    await query.edit_message_text(text, parse_mode="Markdown")

# --- ЗАПУСК ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(punch, pattern="punch"))
    app.add_handler(CallbackQueryHandler(more, pattern="more"))

    print("✅ Бот Балда v2.0 запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
