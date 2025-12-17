import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("Не найден TELEGRAM_BOT_TOKEN в переменных окружения!")


# ==================== КОМАНДА /start ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start с приветствием и главным меню"""
    user = update.effective_user

    welcome_text = f"""
🤖 *Привет, {user.first_name}!*

Я AI-агент *Сергея Зисмана* — эксперта по внедрению AI-решений и автоматизации для B2B-бизнеса.

Здесь ты можешь:
• Узнать о Сергее и его подходе
• Изучить программы и услуги
• Получить контакты для связи
• Записаться на консультацию

_Выбери интересующий раздел из меню ниже_ 👇
"""

    # Создаем клавиатуру с кнопками
    keyboard = [
        [InlineKeyboardButton("👤 О Сергее", callback_data='about')],
        [InlineKeyboardButton("📋 Программы и услуги", callback_data='programs')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contact')],
        [InlineKeyboardButton("💼 Кейсы", callback_data='cases')],
        [InlineKeyboardButton("📅 Записаться на консультацию", callback_data='consultation')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


# ==================== КОМАНДА /about ====================
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация об эксперте"""
    about_text = """
👤 *О Сергее Зисмане*

Меня зовут *Сергей Зисман*. Я помогаю B2B-сервисам и экспертам внедрять AI так, чтобы это влияло на цифры, а не оставалось "интересным экспериментом".

🎯 *Моя специализация:*
• AI-агенты и автоматизации под продажи, поддержку и контент
• Быстрые внутренние инструменты через вайбкодинг

💡 *Мой подход:*
Я беру задачу, превращаю её в понятный процесс и делаю систему, которая работает каждый день.

🔗 *Почему это работает в B2B:*
Я строю агентов вокруг ключевых точек:
⚡ Скорость реакции
💡 Качество первых вопросов
🔍 Точность попадания в задачу
📈 Процесс до решения

_А не вокруг "умных ответов"_
"""

    keyboard = [[InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )


# ==================== КОМАНДА /programs ====================
async def programs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Список программ и услуг"""
    programs_text = """
📋 *Что я внедряю*

*1️⃣ AI-агенты для продаж в B2B*

Когда лидов вроде бы хватает, но "встречи не ставятся" и менеджеры тонут в переписке.

*Агент умеет:*
✓ Задавать вопросы и квалифицировать по твоим критериям
✓ Собирать вводные для КП и созвона
✓ Отвечать на типовые возражения и доводить до следующего шага
✓ Фиксировать всё в CRM

*Результат:* меньше потерь на первом касании и быстрее переход от интереса к разговору.

─────────────────

*2️⃣ AI-агенты для поддержки клиентов*

Когда команда делает одно и то же: "а где инструкция", "а как оплатить", "а что входит".

*Агент:*
✓ Отвечает по базе знаний и регламентам
✓ Просит недостающие данные
✓ Отделяет простые обращения от сложных

*Результат:* ниже нагрузка, выше скорость ответов, меньше раздражения у клиентов.
"""

    keyboard = [
        [InlineKeyboardButton("▶️ Следующая страница", callback_data='programs_2')],
        [InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            programs_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            programs_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )


async def programs_page_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вторая страница программ"""
    programs_text = """
📋 *Что я внедряю* (продолжение)

*3️⃣ AI-агенты для экспертов: контент и воронка*

Когда ты эксперт, и главная проблема не "что сказать", а как стабильно выдавать это в продажу.

*Агент помогает:*
✓ Упаковывать оффер и формулировать "почему покупают"
✓ Делать контент-план под твою воронку
✓ Писать сценарии видео, письма, лендинг-блоки
✓ Сохранять единый стиль и логику

*Результат:* регулярность, ясность, меньше ручной работы, больше системности.

─────────────────

*4️⃣ Вайбкодинг: быстрые инструменты*

Если тебе нужен не "стартап на год", а инструмент, который начинает экономить время сейчас:

✓ Мини-панель для команды
✓ Генератор КП/брифов/скриптов
✓ Внутренний ассистент по базе знаний
✓ Прототип сервиса для клиентов
"""

    keyboard = [
        [InlineKeyboardButton("◀️ Предыдущая страница", callback_data='programs')],
        [InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        programs_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


# ==================== КОМАНДА /contact ====================
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Контактная информация"""
    contact_text = """
📞 *Контакты*

Свяжись со мной удобным способом:

🔹 *Telegram:* [@sergeyzisman](https://t.me/sergeyzisman)
🔹 *WhatsApp:* [+972 58 630 5753](https://wa.me/972586305753)
🔹 *LinkedIn:* [Sergey Zisman](https://www.linkedin.com/in/sergeyzisman/)
🔹 *Сайт:* [sergeyzisman.tech](https://sergeyzisman.tech/)

💬 Напиши мне напрямую или запишись на бесплатную консультацию!
"""

    keyboard = [[InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            contact_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            contact_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )


# ==================== КОМАНДА /cases ====================
async def cases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кейсы и примеры работ"""
    cases_text = """
💼 *Кейсы и примеры работ*

🎯 *Тебе ко мне, если:*

✅ Лиды есть, но конверсия в созвон слабая
✅ Менеджеры перегружены и пропускают тёплых
✅ Поддержка съедает день и мешает росту
✅ Контент нужен постоянно, но ты не хочешь жить в контент-мясорубке
✅ Хочется системно, быстро, без лишней разработки

─────────────────

🔥 *Примеры реализованных решений:*

• Квалификационный бот для B2B-сервиса
• AI-помощник в поддержку с базой знаний
• Контент-генератор для экспертов
• Внутренние инструменты для команды

_Подробнее о кейсах и результатах — пиши в личку!_
"""

    keyboard = [[InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            cases_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            cases_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )


# ==================== КОМАНДА /consultation ====================
async def consultation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запись на консультацию"""
    consultation_text = """
📅 *Записаться на консультацию*

Хочешь разобраться, как AI-агенты могут помочь именно твоему бизнесу?

🎯 *На консультации я:*
1️⃣ Задам 7-10 коротких вопросов
2️⃣ Соберу контекст твоей ситуации
3️⃣ Предложу 2-3 сценария внедрения

📌 *Ты узнаешь:*
✓ Что автоматизировать первым
✓ Какой эффект ожидать
✓ Какие данные нужны для запуска

─────────────────

💬 *Как записаться:*

Напиши мне напрямую в удобный мессенджер:

🔹 [Telegram](https://t.me/sergeyzisman)
🔹 [WhatsApp](https://wa.me/972586305753)

Или отправь сообщение прямо здесь — я получу уведомление!
"""

    keyboard = [
        [InlineKeyboardButton("✍️ Написать Сергею", url='https://t.me/sergeyzisman')],
        [InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            consultation_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            consultation_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )


# ==================== ОБРАБОТЧИК КНОПОК ====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на inline-кнопки"""
    query = update.callback_query
    await query.answer()

    # Маршрутизация по callback_data
    if query.data == 'menu':
        await start_callback(update, context)
    elif query.data == 'about':
        await about(update, context)
    elif query.data == 'programs':
        await programs(update, context)
    elif query.data == 'programs_2':
        await programs_page_2(update, context)
    elif query.data == 'contact':
        await contact(update, context)
    elif query.data == 'cases':
        await cases(update, context)
    elif query.data == 'consultation':
        await consultation(update, context)


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню через callback"""
    user = update.effective_user

    welcome_text = f"""
🤖 *Привет, {user.first_name}!*

Я AI-агент *Сергея Зисмана* — эксперта по внедрению AI-решений и автоматизации для B2B-бизнеса.

Здесь ты можешь:
• Узнать о Сергее и его подходе
• Изучить программы и услуги
• Получить контакты для связи
• Записаться на консультацию

_Выбери интересующий раздел из меню ниже_ 👇
"""

    keyboard = [
        [InlineKeyboardButton("👤 О Сергее", callback_data='about')],
        [InlineKeyboardButton("📋 Программы и услуги", callback_data='programs')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contact')],
        [InlineKeyboardButton("💼 Кейсы", callback_data='cases')],
        [InlineKeyboardButton("📅 Записаться на консультацию", callback_data='consultation')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================
def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("programs", programs))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("cases", cases))
    application.add_handler(CommandHandler("consultation", consultation))

    # Регистрируем обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запускаем бота
    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
