import google.generativeai as genai
import random
from config import Config

# Настройка Gemini
genai.configure(api_key=Config.OPENAI_API_KEY)


class AIContentGenerator:
    @staticmethod
    def generate_post_text(theme=None):
        if not theme:
            theme = random.choice(Config.THEMES)

        # Разные стили постов для вариативности
        styles = [
            "новостной стиль с актуальной информацией",
            "образовательный стиль с практическими советами",
            "аналитический стиль с разбором кейсов",
            "экспертный стиль с прогнозами и трендами",
            "практический стиль с пошаговыми инструкциями",
        ]

        formats = [
            "проблема → решение → рекомендации",
            "факты → анализ → выводы",
            "тренды → вызовы → возможности",
            "угрозы → защита → профилактика",
            "теория → практика → результаты",
        ]

        style = random.choice(styles)
        format_type = random.choice(formats)

        prompt = f"""
        Напиши УНИКАЛЬНЫЙ пост для Telegram канала о кибербезопасности на тему "{theme}".
        
        СТИЛЬ: {style}
        ФОРМАТ: {format_type}
        
        Конкретные требования:
        - Начни с цепляющего заголовка с эмодзи
        - 2-3 коротких абзаца разного содержания
        - Добавь конкретные примеры или кейсы
        - Включи практические рекомендации
        - Используй разные эмодзи в каждом абзаце
        - Закончи вопросом к аудитории
        - Добавь 3-5 релевантных хештегов
        
        Сделай каждый пост максимально уникальным и полезным!
        """

        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=600,
                    temperature=0.9,  # Увеличили температуру для большей креативности
                    top_p=0.8,
                ),
            )

            return response.text

        except Exception as e:
            print(f"❌ Ошибка Gemini API: {e}")
            return AIContentGenerator._get_fallback_post(theme)

    @staticmethod
    def _get_fallback_post(theme):
        """Резервные посты с большей вариативностью"""
        fallbacks = [
            f"""🔐 **{theme}: Новые вызовы 2024**

С развитием технологий появляются и новые угрозы. {theme} требует постоянного обновления подходов к защите.

💡 Ключевые аспекты:
• Мониторинг угроз в реальном времени
• Автоматизация процессов безопасности  
• Обучение сотрудников

🚀 Какие инструменты используете для защиты? Делитесь в комментариях!

#{theme.replace(" ", "")} #Кибербезопасность #ЗащитаДанных""",
            f"""🛡️ **{theme}: Лучшие практики**

В современном цифровом мире {theme.lower()} становится критически важной. Рассмотрим эффективные методы защиты.

⚡ Актуальные тренды:
• Проактивная безопасность
• Zero Trust подход
• AI-ассистированная защита

💬 Как вы решаете вопросы {theme.lower()}? Интересен ваш опыт!

#{theme.replace(" ", "")} #Security #Безопасность""",
            f"""💻 **{theme}: Экспертный взгляд**

{theme} - одна из самых динамичных областей ИБ. Ежедневно появляются новые векторы атак и методы защиты.

🔒 Рекомендации:
• Регулярные обновления систем
• Многофакторная аутентификация
• Резервное копирование данных

📊 Сталкивались с {theme.lower()}? Расскажите о своем опыте!

#{theme.replace(" ", "")} #InfoSec #Киберзащита""",
        ]
        return random.choice(fallbacks)

    @staticmethod
    def generate_image(prompt):
        """Генерация случайного изображения"""
        image_ids = random.sample(range(1000, 9999), 5)
        return f"https://picsum.photos/1024/1024?random={random.choice(image_ids)}"

    @staticmethod
    def generate_image_prompt(post_text):
        """Генерация промпта для изображения"""
        cyber_prompts = [
            "futuristic cybersecurity concept digital shield protecting data glowing blue security grid abstract technology background",
            "cyber security protection digital lock and firewall network security concept glowing particles dark background",
            "data encryption concept digital code flowing through secure tunnel abstract cybersecurity art modern design",
            "hacker protection digital defense system cyber attack prevention futuristic security technology neon lights",
            "zero trust architecture multiple verification layers digital authentication process abstract security concept",
            "phishing attack prevention digital fishing hook with lock cybersecurity metaphor glowing elements dark theme",
            "network security monitoring digital radar detecting threats cyber defense system futuristic interface",
        ]
        return random.choice(cyber_prompts)
