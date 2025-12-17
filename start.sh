#!/bin/bash

echo "🤖 Запуск AI Agent Bot..."
echo ""

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env из .env.example и добавьте токен бота"
    echo ""
    echo "Команды:"
    echo "  cp .env.example .env"
    echo "  nano .env  # или используйте любой редактор"
    exit 1
fi

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
    echo ""
fi

# Активация виртуального окружения
echo "🔄 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install -q -r requirements.txt
echo "✅ Зависимости установлены"
echo ""

# Загрузка переменных окружения
export $(cat .env | grep -v '^#' | xargs)

# Запуск бота
echo "🚀 Запуск бота..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
python bot.py
