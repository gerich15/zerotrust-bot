import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Telegram
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL")

    # Google Gemini (теперь используем этот ключ)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Settings
    POST_INTERVAL = int(os.getenv("POST_INTERVAL_HOURS", 6))

    # Темы только по кибербезопасности
    THEMES = [
        "Zero Trust архитектура",
        "фишинг и социальная инженерия",
        "криптография и шифрование",
        "сетевая безопасность",
        "безопасность приложений",
        "киберпреступность и расследования",
        "защита данных и GDPR",
        "пентестинг и этичный хакинг",
        "безопасность IoT устройств",
        "искусственный интеллект в кибербезопасности",
    ]
