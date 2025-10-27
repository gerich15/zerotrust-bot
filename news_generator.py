import openai
import random
from datetime import datetime, timedelta
from config import Config

openai.api_key = Config.OPENAI_API_KEY


class NewsGenerator:
    @staticmethod
    def generate_cybersecurity_news():
        """Генерирует новости о кибербезопасности"""

        news_types = [
            "новое уязвимость и патч",
            "кибератака на крупную компанию",
            "новый инструмент для пентеста",
            "изменения в законодательстве",
            "отчет о трендах кибербезопасности",
            "интервью с экспертом по безопасности",
        ]

        news_type = random.choice(news_types)

        prompt = f"""
        Напиши короткую новость для Telegram канала о кибербезопасности.
        
        Тип новости: {news_type}
        Формат: заголовок → краткое описание → последствия → рекомендации
        Стиль: новостной, информативный, с элементами анализа
        Длина: 150-250 слов
        Добавь эмодзи где уместно
        Хештеги: {", ".join(random.sample(Config.HASHTAGS, 4))}
        
        Сделай новость актуальной и полезной для специалистов по безопасности.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты новостной редактор специализированного издания по кибербезопасности.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=400,
            )

            return f"📰 КИБЕРНОВОСТИ:\n\n{response.choices[0].message.content.strip()}"
        except:
            return "🚨 Актуальные новости кибербезопасности! Следите за обновлениями. #Киберновости #Безопасность"
