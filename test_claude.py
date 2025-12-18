#!/usr/bin/env python3
"""
Test script to verify Claude API connectivity
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Test answers similar to what the bot would send
test_answers = [
    {
        "question_number": 1,
        "question_text": "Расскажи о своем бизнесе: чем занимаешься и в какой нише работаешь?",
        "answer": "Онлайн-школа по обучению дизайну"
    },
    {
        "question_number": 2,
        "question_text": "Сколько человек в твоей команде и какие основные роли?",
        "answer": "5 человек: я, менеджер, два преподавателя, маркетолог"
    },
    {
        "question_number": 3,
        "question_text": "Какие процессы/задачи сейчас отнимают больше всего времени у тебя или команды?",
        "answer": "Обработка заявок и ответы на вопросы студентов"
    },
    {
        "question_number": 4,
        "question_text": "Какие у тебя есть системы (CRM, таск-менеджер, база клиентов)?",
        "answer": "Notion, Telegram"
    },
    {
        "question_number": 5,
        "question_text": "Работаешь ли ты с клиентами напрямую? Если да, то как обычно происходит коммуникация?",
        "answer": "Да, через Telegram и email"
    },
    {
        "question_number": 6,
        "question_text": "Есть ли у тебя повторяющиеся задачи, которые делаешь вручную (отчёты, письма, анализ)?",
        "answer": "Да, еженедельные отчеты и рассылки"
    },
    {
        "question_number": 7,
        "question_text": "Какой примерный бюджет готов выделить на автоматизацию в месяц?",
        "answer": "До 50 000 рублей"
    }
]

def test_claude_api():
    """Test Claude API with sample answers"""

    api_key = os.getenv('ANTHROPIC_API_KEY')
    print(f"API Key found: {api_key[:20]}..." if api_key else "API Key NOT found!")

    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in environment variables")
        return

    try:
        # Initialize client
        print("\n1. Initializing Anthropic client...")
        client = Anthropic(api_key=api_key)
        print("✓ Client initialized successfully")

        # Build context
        print("\n2. Building context from answers...")
        context = "Ответы клиента:\n\n"
        for answer in test_answers:
            context += f"Вопрос {answer['question_number']}: {answer['question_text']}\n"
            context += f"Ответ: {answer['answer']}\n\n"

        print(f"✓ Context built ({len(context)} characters)")

        # Build prompt
        print("\n3. Building prompt...")
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

        print(f"✓ Prompt built ({len(prompt)} characters)")

        # Try multiple models to see which one works
        models_to_try = [
            "claude-3-5-sonnet-20241022",  # Latest Sonnet 3.5
            "claude-3-5-sonnet-20240620",  # Previous Sonnet 3.5
            "claude-3-sonnet-20240229",    # Sonnet 3
            "claude-3-opus-20240229",      # Opus (fallback)
            "claude-3-haiku-20240307"      # Haiku (cheapest)
        ]

        message = None
        working_model = None

        for model_name in models_to_try:
            try:
                print(f"\n4. Trying model: {model_name}...")

                message = client.messages.create(
                    model=model_name,
                    max_tokens=2500,
                    temperature=0.7,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                print(f"✓ API call successful with model: {model_name}")
                working_model = model_name
                break

            except Exception as model_error:
                print(f"✗ Model {model_name} failed: {str(model_error)[:100]}")
                continue

        if not message:
            print("\n❌ All models failed!")
            return False

        # Extract response
        print("\n5. Extracting response...")
        response_text = message.content[0].text
        print(f"✓ Response received ({len(response_text)} characters)")

        print("\n" + "="*60)
        print(f"WORKING MODEL: {working_model}")
        print("="*60)
        print("CLAUDE RESPONSE:")
        print("="*60)
        print(response_text)
        print("="*60)

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"Message: {str(e)}")

        # Print detailed error info
        if hasattr(e, '__dict__'):
            print("\nError details:")
            for key, value in e.__dict__.items():
                print(f"  {key}: {value}")

        return False

if __name__ == "__main__":
    print("="*60)
    print("CLAUDE API TEST SCRIPT")
    print("="*60)

    success = test_claude_api()

    print("\n" + "="*60)
    if success:
        print("✓ TEST PASSED - Claude API is working correctly")
    else:
        print("❌ TEST FAILED - There is an issue with Claude API")
    print("="*60)
