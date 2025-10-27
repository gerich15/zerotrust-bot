import asyncio
import logging
import random
from datetime import datetime
from ai_generator import AIContentGenerator
from news_generator import NewsGenerator  # Добавляем импорт


class PostScheduler:
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.is_running = False

    async def create_and_send_post(self):
        try:
            logging.info("🔄 Создание поста о кибербезопасности...")

            # Чередуем обычные посты и новости (50/50)
            if random.random() > 0.5:
                # Обычный образовательный пост
                post_text = AIContentGenerator.generate_post_text()
                image_prompt = AIContentGenerator.generate_image_prompt(post_text)
            else:
                # Новостной пост
                post_text = NewsGenerator.generate_cybersecurity_news()
                image_prompt = "cybersecurity news, digital newspaper, breaking news about hackers, futuristic news background"

            image_url = AIContentGenerator.generate_image(image_prompt)

            await self.bot.send_photo(
                chat_id=self.channel_id, photo=image_url, caption=post_text
            )

            logging.info(f"✅ Пост о кибербезопасности отправлен в {datetime.now()}")

        except Exception as e:
            logging.error(f"❌ Ошибка: {e}")

    async def start_scheduler(self, interval_hours=6):
        self.is_running = True
        logging.info(
            f"🚀 Планировщик кибербезопасности запущен. Интервал: {interval_hours} часов"
        )

        while self.is_running:
            await self.create_and_send_post()
            await asyncio.sleep(interval_hours * 3600)

    def stop_scheduler(self):
        self.is_running = False
