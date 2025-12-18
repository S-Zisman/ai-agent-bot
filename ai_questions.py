"""
Модуль с вопросами для AI-агента и логикой взаимодействия с Claude API
"""

from typing import List, Dict
from anthropic import Anthropic
import os

# Список вопросов для квалификации клиента
QUESTIONS = [
    {
        "number": 1,
        "text": "Расскажи о своем бизнесе: чем занимаешься и в какой нише работаешь?",
        "type": "open"
    },
    {
        "number": 2,
        "text": "Сколько человек в твоей команде и какие основные роли?",
        "type": "open"
    },
    {
        "number": 3,
        "text": "Какие процессы/задачи сейчас отнимают больше всего времени у тебя или команды?",
        "type": "open"
    },
    {
        "number": 4,
        "text": "Какие у тебя есть системы (CRM, таск-менеджер, база клиентов)?",
        "type": "open"
    },
    {
        "number": 5,
        "text": "Работаешь ли ты с клиентами напрямую? Если да, то как обычно происходит коммуникация?",
        "type": "open"
    },
    {
        "number": 6,
        "text": "Есть ли у тебя повторяющиеся задачи, которые делаешь вручную (отчёты, письма, анализ)?",
        "type": "open"
    },
    {
        "number": 7,
        "text": "Какой примерный бюджет готов выделить на автоматизацию в месяц?",
        "type": "open"
    }
]


class AIAgent:
    """Класс для взаимодействия с Claude API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY не найден!")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"  # Claude 3 Haiku - быстрая и дешевая модель

    def generate_scenarios(self, answers: List[Dict]) -> str:
        """
        Генерация 2-3 сценариев внедрения на основе ответов пользователя

        Args:
            answers: Список ответов пользователя с вопросами

        Returns:
            Отформатированный текст со сценариями
        """

        # Формируем контекст из ответов
        context = "Ответы клиента:\n\n"
        for answer in answers:
            context += f"Вопрос {answer['question_number']}: {answer['question_text']}\n"
            context += f"Ответ: {answer['answer']}\n\n"

        # Промпт для Claude
        prompt = f"""Ты — эксперт по внедрению AI-решений и автоматизации для B2B-бизнеса.

На основе ответов клиента проанализируй его ситуацию и предложи 2-3 конкретных сценария внедрения AI и автоматизации.

{context}

Для каждого сценария укажи:
1. **Название сценария** (короткое, ёмкое)
2. **Что автоматизируем** (конкретные процессы)
3. **Ожидаемый эффект** (экономия времени, рост конверсии, снижение нагрузки и т.д.)
4. **Какие данные/системы нужны** для реализации
5. **Срок внедрения** (ориентировочно)

Сценарии должны быть:
- Практичными и реализуемыми
- Ранжированы по приоритету (от самого важного к менее приоритетному)
- Адаптированы под размер бизнеса и бюджет клиента
- Написаны простым языком, без технического жаргона

Формат ответа: структурированный текст с эмодзи для визуальной привлекательности."""

        # Запрос к Claude API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Извлекаем текст ответа
        return message.content[0].text

    def get_question_by_number(self, number: int) -> Dict:
        """Получить вопрос по номеру"""
        for q in QUESTIONS:
            if q['number'] == number:
                return q
        return None

    def get_total_questions(self) -> int:
        """Получить общее количество вопросов"""
        return len(QUESTIONS)

    def format_question(self, number: int) -> str:
        """Отформатировать вопрос для отправки пользователю"""
        question = self.get_question_by_number(number)
        if not question:
            return None

        total = self.get_total_questions()
        return f"*Вопрос {number}/{total}:*\n\n{question['text']}"
