# Деплой AI Agent Bot на VPS

Инструкция по развертыванию бота на VPS (Ubuntu/Debian).

## Подготовка сервера

### 1. Подключение к серверу

```bash
ssh your_user@your_server_ip
```

### 2. Обновление системы

```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Установка Python и зависимостей

```bash
sudo apt install python3 python3-pip python3-venv git -y
```

## Установка бота

### 1. Клонирование репозитория (или загрузка файлов)

```bash
cd /home/your_user
git clone https://github.com/your-username/ai-agent-bot.git
# или создайте папку и загрузите файлы
```

### 2. Переход в папку проекта

```bash
cd ai-agent-bot
```

### 3. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

```bash
cp .env.example .env
nano .env
```

Добавьте ваш токен:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

Сохраните файл: `Ctrl + O`, затем `Enter`, затем `Ctrl + X`

## Запуск бота

### Вариант 1: Screen (простой способ)

```bash
# Установка screen (если не установлен)
sudo apt install screen -y

# Создание новой screen-сессии
screen -S telegram-bot

# Запуск бота
python bot.py

# Отключение от сессии: Ctrl + A, затем D
# Возврат к сессии: screen -r telegram-bot
# Остановка бота: screen -r telegram-bot, затем Ctrl + C
```

### Вариант 2: Systemd Service (рекомендуется для продакшена)

#### Создание service файла

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

#### Содержимое файла:

```ini
[Unit]
Description=AI Agent Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/ai-agent-bot
Environment="PATH=/home/your_user/ai-agent-bot/venv/bin"
ExecStart=/home/your_user/ai-agent-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Замените `your_user` на ваше имя пользователя!**

#### Запуск сервиса

```bash
# Перезагрузка конфигурации systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable telegram-bot

# Запуск бота
sudo systemctl start telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot

# Просмотр логов
sudo journalctl -u telegram-bot -f
```

#### Управление сервисом

```bash
# Остановка бота
sudo systemctl stop telegram-bot

# Перезапуск бота
sudo systemctl restart telegram-bot

# Отключение автозапуска
sudo systemctl disable telegram-bot
```

### Вариант 3: Docker (будет добавлено позже)

## Обновление бота

```bash
# Если используете screen
screen -r telegram-bot
# Нажмите Ctrl + C для остановки
git pull  # или загрузите новые файлы
python bot.py

# Если используете systemd
cd /home/your_user/ai-agent-bot
git pull  # или загрузите новые файлы
sudo systemctl restart telegram-bot
```

## Мониторинг

### Просмотр логов (systemd)

```bash
# Последние 50 строк
sudo journalctl -u telegram-bot -n 50

# В реальном времени
sudo journalctl -u telegram-bot -f

# За сегодня
sudo journalctl -u telegram-bot --since today
```

### Проверка работы

```bash
# Проверка процесса
ps aux | grep bot.py

# Проверка статуса сервиса
sudo systemctl status telegram-bot

# Проверка использования ресурсов
htop
```

## Безопасность

### 1. Настройка firewall

```bash
sudo ufw allow ssh
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Права доступа к .env

```bash
chmod 600 .env
```

### 3. Регулярные обновления

```bash
sudo apt update && sudo apt upgrade -y
```

## Резервное копирование

### Backup конфигурации

```bash
# Создание резервной копии .env
cp .env .env.backup

# Backup всей папки
tar -czf telegram-bot-backup-$(date +%Y%m%d).tar.gz /home/your_user/ai-agent-bot
```

## Решение проблем

### Бот не запускается

1. Проверьте логи: `sudo journalctl -u telegram-bot -n 50`
2. Проверьте токен в `.env`
3. Проверьте права доступа: `ls -la`
4. Проверьте зависимости: `pip list`

### Бот падает после запуска

1. Проверьте токен бота
2. Проверьте подключение к интернету: `ping telegram.org`
3. Проверьте Python версию: `python --version`

### Высокое потребление ресурсов

1. Проверьте логи на ошибки
2. Мониторьте использование: `htop`
3. Рассмотрите rate limiting

## Интеграция с n8n (на вашем VPS)

Если у вас уже развернут n8n на VPS:

1. Создайте webhook в n8n
2. Добавьте URL webhook в переменные окружения:
   ```bash
   N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/...
   ```
3. Обновите код бота для отправки данных в n8n

---

**Полезные команды:**

```bash
# Перезагрузка сервера
sudo reboot

# Проверка свободного места
df -h

# Проверка памяти
free -h

# Проверка времени работы
uptime
```

---

**Поддержка:** [@sergeyzisman](https://t.me/sergeyzisman)
