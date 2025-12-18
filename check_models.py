#!/usr/bin/env python3
"""
Скрипт для проверки доступных моделей Claude API
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

# Все возможные модели Claude
ALL_MODELS = [
    # Sonnet 3.5
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",

    # Sonnet 3
    "claude-3-sonnet-20240229",

    # Opus 3
    "claude-3-opus-20240229",

    # Haiku 3
    "claude-3-haiku-20240307",
]

def check_model_access():
    """Проверяем доступ к разным моделям"""

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ API ключ не найден")
        return

    print(f"API Key: {api_key[:20]}...")
    print("\n" + "="*60)
    print("ПРОВЕРКА ДОСТУПНЫХ МОДЕЛЕЙ")
    print("="*60 + "\n")

    client = Anthropic(api_key=api_key)
    available_models = []

    for model in ALL_MODELS:
        try:
            # Делаем минимальный запрос
            response = client.messages.create(
                model=model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print(f"✅ {model:<35} - ДОСТУПНА")
            available_models.append(model)

        except Exception as e:
            error_type = type(e).__name__
            if "404" in str(e) or "not_found" in str(e):
                print(f"❌ {model:<35} - НЕТ ДОСТУПА (404)")
            elif "401" in str(e) or "authentication" in str(e).lower():
                print(f"❌ {model:<35} - ОШИБКА АВТОРИЗАЦИИ")
            else:
                print(f"⚠️  {model:<35} - {error_type}")

    print("\n" + "="*60)
    print(f"ДОСТУПНО МОДЕЛЕЙ: {len(available_models)}")
    print("="*60)

    if available_models:
        print("\nРекомендация для бота:")
        # Приоритет: Sonnet 3.5 > Sonnet 3 > Haiku > Opus
        if any("3-5-sonnet" in m for m in available_models):
            recommended = next(m for m in available_models if "3-5-sonnet" in m)
            print(f"🎯 Используй: {recommended}")
            print("   (Быстро, дешево, качественно)")
        elif any("3-sonnet" in m for m in available_models):
            recommended = next(m for m in available_models if "3-sonnet" in m)
            print(f"🎯 Используй: {recommended}")
            print("   (Хороший баланс цены и качества)")
        elif any("haiku" in m for m in available_models):
            recommended = next(m for m in available_models if "haiku" in m)
            print(f"🎯 Используй: {recommended}")
            print("   (Самая дешевая, для простых задач)")
        else:
            recommended = available_models[0]
            print(f"🎯 Используй: {recommended}")

if __name__ == "__main__":
    check_model_access()
