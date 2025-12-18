import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from telegram.constants import ParseMode

# Импортируем наши модули
from database import Database
from ai_questions import AIAgent, QUESTIONS

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

if not BOT_TOKEN:
    raise ValueError("Не найден TELEGRAM_BOT_TOKEN в переменных окружения!")

if not ANTHROPIC_API_KEY:
    raise ValueError("Не найден ANTHROPIC_API_KEY в переменных окружения!")

# Инициализируем базу данных и AI-агента
db = Database()
ai_agent = AIAgent(ANTHROPIC_API_KEY)

# Состояния для ConversationHandler
ASKING_QUESTIONS = 1
GENERATING_SCENARIOS = 2


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
• Пройти диалог с AI-агентом для подбора сценария

_Выбери интересующий раздел из меню ниже_ 👇
"""

    # Создаем клавиатуру с кнопками
    keyboard = [
        [InlineKeyboardButton("👤 О Сергее", callback_data='about')],
        [InlineKeyboardButton("📋 Программы и услуги", callback_data='programs')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contact')],
        [InlineKeyboardButton("💼 Кейсы", callback_data='cases')],
        [InlineKeyboardButton("📅 Записаться на консультацию", callback_data='consultation')],
        [InlineKeyboardButton("🤖 Диалог с AI-агентом", callback_data='start_ai_dialog')],
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


# ==================== AI-ДИАЛОГ: НАЧАЛО ====================
async def start_ai_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало диалога с AI-агентом"""
    query = update.callback_query
    user = update.effective_user

    # Сохраняем пользователя в БД
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    # Создаем новый диалог
    conversation_id = db.start_conversation(user.id)
    context.user_data['conversation_id'] = conversation_id
    context.user_data['current_question'] = 1

    intro_text = """
🤖 *Отлично! Давай разберемся, какие AI-решения подойдут именно тебе*

Я задам тебе *7 коротких вопросов* о твоем бизнесе и процессах.

После этого я проанализирую твои ответы и предложу *2-3 конкретных сценария внедрения* с оценкой эффекта и требований.

_Готов начать? Жми кнопку ниже!_ 👇
"""

    keyboard = [
        [InlineKeyboardButton("✅ Начать диалог", callback_data='ask_first_question')],
        [InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        intro_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

    return ASKING_QUESTIONS


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Задать очередной вопрос пользователю"""
    query = update.callback_query
    await query.answer()

    question_number = context.user_data.get('current_question', 1)
    question_text = ai_agent.format_question(question_number)

    if not question_text:
        # Все вопросы заданы, переходим к генерации сценариев
        return await generate_scenarios(update, context)

    keyboard = [[InlineKeyboardButton("❌ Отменить диалог", callback_data='cancel_dialog')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        question_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

    return ASKING_QUESTIONS


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа пользователя на вопрос"""
    user_answer = update.message.text
    question_number = context.user_data.get('current_question', 1)
    conversation_id = context.user_data.get('conversation_id')

    # Получаем текст вопроса
    question_data = ai_agent.get_question_by_number(question_number)

    # Сохраняем ответ в БД
    db.save_answer(
        conversation_id=conversation_id,
        question_number=question_number,
        question_text=question_data['text'],
        answer=user_answer
    )

    # Переходим к следующему вопросу
    context.user_data['current_question'] = question_number + 1

    # Проверяем, есть ли еще вопросы
    total_questions = ai_agent.get_total_questions()

    if question_number < total_questions:
        # Задаем следующий вопрос
        next_question_text = ai_agent.format_question(question_number + 1)

        keyboard = [[InlineKeyboardButton("❌ Отменить диалог", callback_data='cancel_dialog')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"✅ Принято!\n\n{next_question_text}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

        return ASKING_QUESTIONS
    else:
        # Все вопросы заданы, генерируем сценарии
        await update.message.reply_text(
            "✅ *Отлично! Все ответы получены.*\n\n⏳ Анализирую данные и готовлю сценарии...",
            parse_mode=ParseMode.MARKDOWN
        )

        return await generate_scenarios_from_message(update, context)


async def generate_scenarios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация сценариев внедрения через Claude API"""
    query = update.callback_query
    conversation_id = context.user_data.get('conversation_id')

    # Получаем все ответы из БД
    answers = db.get_conversation_answers(conversation_id)

    # Генерируем сценарии через Claude API
    try:
        scenarios_text = ai_agent.generate_scenarios(answers)

        # Сохраняем сценарии в БД
        db.save_scenarios(conversation_id, [{"text": scenarios_text}])
        db.complete_conversation(conversation_id)

        # Отправляем результат пользователю
        result_message = f"""
🎯 *Анализ завершен! Вот твои персональные сценарии внедрения:*

{scenarios_text}

─────────────────

💬 *Что дальше?*

Если хочешь обсудить детали внедрения — пиши Сергею напрямую:
• [Telegram](https://t.me/sergeyzisman)
• [WhatsApp](https://wa.me/972586305753)
"""

        keyboard = [
            [InlineKeyboardButton("✍️ Написать Сергею", url='https://t.me/sergeyzisman')],
            [InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            result_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Ошибка при генерации сценариев: {e}")
        await query.edit_message_text(
            "❌ Произошла ошибка при генерации сценариев. Попробуй позже или свяжись напрямую с Сергеем.",
            parse_mode=ParseMode.MARKDOWN
        )

    return ConversationHandler.END


async def generate_scenarios_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация сценариев (вызов из обработчика сообщений)"""
    conversation_id = context.user_data.get('conversation_id')

    # Получаем все ответы из БД
    answers = db.get_conversation_answers(conversation_id)

    # Генерируем сценарии через Claude API
    try:
        scenarios_text = ai_agent.generate_scenarios(answers)

        # Сохраняем сценарии в БД
        db.save_scenarios(conversation_id, [{"text": scenarios_text}])
        db.complete_conversation(conversation_id)

        # Отправляем результат пользователю
        result_message = f"""
🎯 *Анализ завершен! Вот твои персональные сценарии внедрения:*

{scenarios_text}

─────────────────

💬 *Что дальше?*

Если хочешь обсудить детали внедрения — пиши Сергею напрямую:
• [Telegram](https://t.me/sergeyzisman)
• [WhatsApp](https://wa.me/972586305753)
"""

        keyboard = [
            [InlineKeyboardButton("✍️ Написать Сергею", url='https://t.me/sergeyzisman')],
            [InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            result_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Ошибка при генерации сценариев: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при генерации сценариев. Попробуй позже или свяжись напрямую с Сергеем.",
            parse_mode=ParseMode.MARKDOWN
        )

    return ConversationHandler.END


async def cancel_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена диалога"""
    query = update.callback_query
    await query.answer()

    cancel_text = """
❌ *Диалог отменен*

Ты всегда можешь начать заново, выбрав "Диалог с AI-агентом" в меню.

Или свяжись напрямую с Сергеем для персональной консультации!
"""

    keyboard = [[InlineKeyboardButton("◀️ Вернуться в меню", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        cancel_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

    return ConversationHandler.END


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
    elif query.data == 'start_ai_dialog':
        return await start_ai_dialog(update, context)
    elif query.data == 'ask_first_question':
        return await ask_question(update, context)
    elif query.data == 'cancel_dialog':
        return await cancel_dialog(update, context)


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
• Пройти диалог с AI-агентом для подбора сценария

_Выбери интересующий раздел из меню ниже_ 👇
"""

    keyboard = [
        [InlineKeyboardButton("👤 О Сергее", callback_data='about')],
        [InlineKeyboardButton("📋 Программы и услуги", callback_data='programs')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contact')],
        [InlineKeyboardButton("💼 Кейсы", callback_data='cases')],
        [InlineKeyboardButton("📅 Записаться на консультацию", callback_data='consultation')],
        [InlineKeyboardButton("🤖 Диалог с AI-агентом", callback_data='start_ai_dialog')],
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

    # Создаем ConversationHandler для AI-диалога
    ai_dialog_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_ai_dialog, pattern='^start_ai_dialog$'),
        ],
        states={
            ASKING_QUESTIONS: [
                CallbackQueryHandler(ask_question, pattern='^ask_first_question$'),
                CallbackQueryHandler(cancel_dialog, pattern='^cancel_dialog$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(cancel_dialog, pattern='^cancel_dialog$'),
            CommandHandler('start', start),
        ],
        allow_reentry=True,
    )

    # Регистрируем ConversationHandler
    application.add_handler(ai_dialog_handler)

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("programs", programs))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("cases", cases))
    application.add_handler(CommandHandler("consultation", consultation))

    # Регистрируем обработчик кнопок (должен быть после ConversationHandler)
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запускаем бота
    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
