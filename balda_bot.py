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

    keyboard = [[InlineKeyboardButton("👊 Пинать Балду", callback_data="punch")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "Привет, Хозяин! 👋\n\nЯ Балда. Я не обещаю лёгких денег. Я показываю, куда идти, чтобы заработать. Пни меня."

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

    keyboard = [
        [InlineKeyboardButton("🔗 Зарегистрироваться в партнёрке Яндекса", url="https://partners-app.yandex.ru/")],
        [InlineKeyboardButton("← Назад", callback_data="punch")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🚚 *Заработок на курьерах*\n\n"
        "Яндекс платит до 31 200 рублей за каждого курьера, который пришёл и работает по твоей ссылке.\n"
        "Ссылку даёт сам Яндекс через партнёрский кабинет.\n\n"
        "Мы создаём и размещаем контент в рилсах и ставим реф\\. ссылку в шапку профиля\\.\n\n"
        "Это бесплатно, но ты должен быть самозанятым или ИП\\.\n\n"
        "👇 Первый шаг — зарегистрируйся в партнёрке:"
    )

    await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=reply_markup)

# --- КОМАНДА /about ---
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("👊 Начать зарабатывать", callback_data="punch")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🤖 *О проекте «Балда»*\n\n"
        "Балда — это цифровой помощник для заработка на курьерских доставках\\.\n\n"
        "📌 *Как это работает:*\n"
        "1\\. Ты регистрируешься в Партнёрке Яндекса\n"
        "2\\. Балда даёт тебе промты для генерации контента\n"
        "3\\. Ты выкладываешь фото/видео и получаешь заказы\n\n"
        "💡 *Концепция:*\n"
        "Балда — персонаж из сказки Пушкина, который стал наставником для тех, "
        "кто хочет зарабатывать без сложных схем\\.\n\n"
        "© Алексей Терентьев, 2026\n"
        "@agterentev"
    )

    await update.message.reply_text(text, parse_mode="MarkdownV2", reply_markup=reply_markup)

# --- НАСТРОЙКА МЕНЮ ---
async def set_commands(app):
    commands = [
        BotCommand("start", "Главное меню"),
        BotCommand("about", "О проекте"),
    ]
    await app.bot.set_my_commands(commands)

# --- ЗАПУСК ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(punch, pattern="punch"))
    app.add_handler(CallbackQueryHandler(more, pattern="more"))

    app.post_init = set_commands

    print("✅ Бот Балда v2.2 запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
