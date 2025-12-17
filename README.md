# AI Agent Bot - Telegram бот-визитка Сергея Зисмана

Telegram-бот для представления услуг AI-агентства и экспертизы по внедрению AI-решений в B2B.

## Возможности бота

### Команды:
- `/start` - Главное меню с интерактивными кнопками
- `/about` - Информация о Сергее Зисмане и его подходе
- `/programs` - Список программ и услуг (AI-агенты, вайбкодинг)
- `/contact` - Контактная информация
- `/cases` - Кейсы и примеры работ
- `/consultation` - Запись на консультацию

### Особенности:
- Интерактивная навигация через inline-кнопки
- Форматирование текста с использованием Markdown
- Эмодзи для улучшения визуального восприятия
- Структурированная информация по услугам
- Прямые ссылки на контакты (Telegram, WhatsApp, LinkedIn, сайт)

## Установка и запуск

### 1. Клонируйте репозиторий или скопируйте файлы

### 2. Создайте виртуальное окружение (рекомендуется)

```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Создайте файл .env

Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

Откройте `.env` и добавьте токен вашего бота:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

### 5. Получите токен бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в файл `.env`

### 6. Настройте команды бота (опционально)

Отправьте [@BotFather](https://t.me/BotFather) команду `/setcommands`, выберите вашего бота и вставьте:

```
start - Главное меню
about - О Сергее Зисмане
programs - Программы и услуги
contact - Контакты
cases - Кейсы и примеры работ
consultation - Записаться на консультацию
```

### 7. Запустите бота

```bash
python bot.py
```

Бот запустится и будет готов к приему сообщений!

## Структура проекта

```
ai-agent-bot/
├── bot.py              # Основной файл бота
├── requirements.txt    # Зависимости Python
├── .env.example        # Пример файла с переменными окружения
├── .gitignore         # Исключения для Git
└── README.md          # Документация
```

## Технологии

- **Python 3.8+**
- **python-telegram-bot 20.7** - современная библиотека для работы с Telegram Bot API
- **python-dotenv** - загрузка переменных окружения из .env файла

## Контакты эксперта

- **Telegram:** [@sergeyzisman](https://t.me/sergeyzisman)
- **WhatsApp:** [+972 58 630 5753](https://wa.me/972586305753)
- **LinkedIn:** [Sergey Zisman](https://www.linkedin.com/in/sergeyzisman/)
- **Сайт:** [sergeyzisman.tech](https://sergeyzisman.tech/)

## Деплой на VPS

Для запуска бота на сервере:

### Вариант 1: Простой запуск через screen/tmux

```bash
screen -S telegram-bot
python bot.py
# Нажмите Ctrl+A, затем D для выхода из screen
```

### Вариант 2: Systemd service

Создайте файл `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=AI Agent Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ai-agent-bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Запустите сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### Вариант 3: Docker (будет добавлено позже)

## Интеграция с n8n

Для расширенных возможностей (CRM, аналитика, автоматизация) можно интегрировать с n8n:

1. Добавить webhook в n8n
2. Отправлять события из бота в n8n
3. Обрабатывать заявки и контакты через workflow

_Детальная инструкция по интеграции будет добавлена позже._

## Разработка

Для локальной разработки:

1. Установите зависимости для разработки (если будут)
2. Используйте тестовый токен бота
3. Включите debug-режим в логировании

## Лицензия

Создано для демонстрации возможностей вайбкодинга и AI-решений.

---

Создано с помощью AI для демонстрации возможностей вайбкодинга
