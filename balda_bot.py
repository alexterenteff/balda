import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
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

    keyboard = [[InlineKeyboardButton("👊 Пинать Балду", callback_data="punch")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"Привет, {name}! 👋\n\nЯ Балда, пни меня, чтобы зарабатывать деньги."

    await update.message.reply_text(text, reply_markup=reply_markup)

# --- КОГДА НАЖАЛИ "Пинать Балду" ---
async def punch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("📖 Подробнее", callback_data="more")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "💰 Заработок на курьерах"

    await query.edit_message_text(text, reply_markup=reply_markup)

# --- КОГДА НАЖАЛИ "Подробнее" ---
async def more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🚚 *Заработок на курьерах*\n\n"
        "Яндекс платит до 31200 рублей за каждого курьера, который пришел и работает по твоей ссылке.\n"
        "Ссылку дает сам Яндекс через партнерский кабинет (реф.ссылка).\n\n"
        "Мы создаем и размещаем контент в рилсах и ставим реф.ссылку в шапку профиля.\n\n"
        "Это все бесплатно, но ты должен быть самозанятым или ИП"
    )

    await query.edit_message_text(text, parse_mode="Markdown")

# --- НОВАЯ КОМАНДА /about (О проекте) ---
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *О проекте «Балда»*\n\n"
        "Балда — это цифровой помощник для заработка на курьерских доставках.\n\n"
        "📌 *Как это работает:*\n"
        "1. Ты регистрируешься в Партнерке Яндекса\n"
        "2. Балда даёт тебе промты для генерации контента\n"
        "3. Ты выкладываешь фото/видео и получаешь заказы\n\n"
        "💡 *Концепция:*\n"
        "Балда — это персонаж из сказки Пушкина, который стал наставником для тех, "
        "кто хочет зарабатывать без сложных схем.\n\n"
        "© Алексей Терентьев, 2026\n"
        "@agterentev»\n\n"
        "Напиши /start, чтобы начать зарабатывать."
    )

    await update.message.reply_text(text, parse_mode="Markdown")

# --- НАСТРОЙКА МЕНЮ ВНИЗУ (постоянные кнопки) ---
async def set_commands(app):
    commands = [
        BotCommand("start", "Главное меню"),
        BotCommand("about", "О проекте"),
    ]
    await app.bot.set_my_commands(commands)

# --- ЗАПУСК ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))

    # Кнопки (callback)
    app.add_handler(CallbackQueryHandler(punch, pattern="punch"))
    app.add_handler(CallbackQueryHandler(more, pattern="more"))

    # Устанавливаем меню с кнопками при старте
    app.post_init = set_commands

    print("✅ Бот Балда v2.1 запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
