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
    name = "Хозяин"

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

    keyboard = [
        [InlineKeyboardButton("📱 Регистрация в Яндексе", url="https://partners-app.yandex.ru/")],
        [InlineKeyboardButton("➡️ Жми сюда после регистрации", callback_data="to_instagram")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🚚 *Заработок на курьерах*\n\n"
        "Яндекс платит до 31200 рублей за каждого курьера, который пришел и работает по твоей ссылке.\n"
        "Ссылку дает сам Яндекс через партнерский кабинет (реф.ссылка).\n\n"
        "Мы создаем и размещаем контент в рилсах и ставим реф.ссылку в шапку профиля.\n\n"
        "Это все бесплатно, но ты должен быть самозанятым или ИП"
    )

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- КОГДА НАЖАЛИ "Жми сюда после регистрации" (ЭКРАН ИНСТАГРАМ) ---
async def to_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ТРИ КНОПКИ
    keyboard = [
        [InlineKeyboardButton("⚙️ Настройка Инстаграм", callback_data="setup_instagram")],
        [InlineKeyboardButton("🤖 Промты для ИИ", callback_data="prompts")],
        [InlineKeyboardButton("🏠 Вернуться в меню", callback_data="to_start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "📸 *Инстаграм*\n\n"
        "Создай новый профиль в Instagram.\n\n"
        "Название профиля должно быть связано с доставкой или курьерской работой.\n"
        "Добавь фото, описание и готовься к загрузке контента."
    )

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- НОВАЯ ФУНКЦИЯ: НАСТРОЙКА ИНСТАГРАМ ---
async def setup_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Кнопка "Вернуться в Инстаграм"
    keyboard = [[InlineKeyboardButton("🔙 Назад в Инстаграм", callback_data="to_instagram")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "⚙️ *Настройка Инстаграм*\n\n"
        "Выполни эти шаги, чтобы подготовить профиль:\n\n"
        "1️⃣ *Реф.ссылка*\n"
        "Добавь ссылку, полученную от Яндекс Партнёрки, в шапку профиля (поле «Веб-сайт»).\n\n"
        "2️⃣ *Фото профиля*\n"
        "Загрузи аватарку. Подойдёт нейтральное или курьерское фото.\n\n"
        "3️⃣ *Имя профиля*\n"
        "Укажи имя, связанное с доставкой (например: \n«Доставка [Твой город]»).\n\n"
        "4️⃣ *Био (описание)*\n"
        "Напиши краткое описание. Пример:\n"
        "`📦 Доставка в [Твой город] без выходных.\n"
        "💸 Промокод: BALDA на скидку 20% на первый заказ.\n"
        "⬇️ Заказы тут: ссылка в шапке`\n\n"
        "✅ После настройки возвращайся и бери промты."
    )

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- ФУНКЦИЯ: ПРОМТЫ ДЛЯ ИИ ---
async def prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("🔙 Назад в Инстаграм", callback_data="to_instagram")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🤖 *Промты для генерации контента*\n\n"
        "Скопируй и вставь в нейросеть (Midjourney, Runway, Sora):\n\n"
        "📸 *Для фото:*\n"
        "`Счастливый курьер с доставкой у ресторана. Вечерний город. Яркий свет. Фотореализм.`\n\n"
        "🎥 *Для видео:*\n"
        "`Курьер выходит из ресторана с заказом, улыбается, садится на велосипед. Динамика.`\n\n"
        "📱 *Для сторис:*\n"
        "`Человек берёт телефон, на экране приложение доставки. Рука с телефоном, размытый фон.`\n\n"
        "🔥 *Для рилс:*\n"
        "`Счастливый клиент получает заказ, курьер улыбается, вокруг летят листья.`\n\n"
        "👉 Генерируй контент, загружай в Инстаграм и зарабатывай!"
    )

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# --- КОГДА НАЖАЛИ "Вернуться в меню" ---
async def to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    name = "Хозяин"

    keyboard = [[InlineKeyboardButton("👊 Пинать Балду", callback_data="punch")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"Привет, {name}! 👋\n\nЯ Балда, пни меня, чтобы зарабатывать деньги."

    await query.edit_message_text(text, reply_markup=reply_markup)

# --- КОМАНДА /about (О проекте) ---
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *О проекте «Балда»*\n\n"
        "Балда — это цифровой помощник для заработка\n\n"
        "© Алексей Терентьев, 2026\n"
        "@agterentev\n\n"
        "Напиши /start, чтобы начать зарабатывать."
    )

    await update.message.reply_text(text, parse_mode="Markdown")

# --- НАСТРОЙКА МЕНЮ ВНИЗУ ---
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
    app.add_handler(CallbackQueryHandler(to_instagram, pattern="to_instagram"))
    app.add_handler(CallbackQueryHandler(setup_instagram, pattern="setup_instagram"))
    app.add_handler(CallbackQueryHandler(prompts, pattern="prompts"))
    app.add_handler(CallbackQueryHandler(to_start, pattern="to_start"))

    app.post_init = set_commands

    print("✅ Бот Балда v2.4 запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
