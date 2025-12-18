import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List

class Database:
    """Класс для работы с SQLite базой данных"""

    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица для хранения пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица для хранения диалогов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT DEFAULT 'in_progress',
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # Таблица для хранения ответов на вопросы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                question_number INTEGER,
                question_text TEXT,
                answer TEXT,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')

        # Таблица для хранения сгенерированных сценариев
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                scenarios_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, user_id: int, username: str = None,
                 first_name: str = None, last_name: str = None):
        """Добавление или обновление пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))

        conn.commit()
        conn.close()

    def start_conversation(self, user_id: int) -> int:
        """Начать новый диалог для пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO conversations (user_id, status)
            VALUES (?, 'in_progress')
        ''', (user_id,))

        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return conversation_id

    def save_answer(self, conversation_id: int, question_number: int,
                    question_text: str, answer: str):
        """Сохранить ответ на вопрос"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO conversation_answers
            (conversation_id, question_number, question_text, answer)
            VALUES (?, ?, ?, ?)
        ''', (conversation_id, question_number, question_text, answer))

        conn.commit()
        conn.close()

    def get_conversation_answers(self, conversation_id: int) -> List[Dict]:
        """Получить все ответы для диалога"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT question_number, question_text, answer, answered_at
            FROM conversation_answers
            WHERE conversation_id = ?
            ORDER BY question_number
        ''', (conversation_id,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def complete_conversation(self, conversation_id: int):
        """Завершить диалог"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE conversations
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (conversation_id,))

        conn.commit()
        conn.close()

    def save_scenarios(self, conversation_id: int, scenarios: List[Dict]):
        """Сохранить сгенерированные сценарии"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        scenarios_json = json.dumps(scenarios, ensure_ascii=False)

        cursor.execute('''
            INSERT INTO scenarios (conversation_id, scenarios_json)
            VALUES (?, ?)
        ''', (conversation_id, scenarios_json))

        conn.commit()
        conn.close()

    def get_user_conversations(self, user_id: int) -> List[Dict]:
        """Получить все диалоги пользователя"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, started_at, completed_at, status
            FROM conversations
            WHERE user_id = ?
            ORDER BY started_at DESC
        ''', (user_id,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_active_conversation(self, user_id: int) -> Optional[int]:
        """Получить активный диалог пользователя (если есть)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id FROM conversations
            WHERE user_id = ? AND status = 'in_progress'
            ORDER BY started_at DESC
            LIMIT 1
        ''', (user_id,))

        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None
