import logging
import random
import schedule
import time
import threading
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import Config

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

print("🔧 ЗАПУСК AI BOT")


class AIPosterBot:
    def __init__(self):
        print("🔧 Инициализация бота...")
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        print("✅ Приложение создано")
        self.auto_posting = False
        self.scheduler_thread = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 AI Poster Bot запущен!\n\n"
            "Команды:\n"
            "/post - Создать и отправить пост\n"
            "/start_auto - Запустить авто-постинг\n"
            "/stop_auto - Остановить авто-постинг\n"
            "/test - Тестовая генерация поста"
        )

    async def create_auto_post(self):
        """Создает и отправляет пост автоматически"""
        try:
            print("🔄 Авто-генерация поста...")
            from ai_generator import AIContentGenerator

            theme = random.choice(Config.THEMES)
            print(f"Тема: {theme}")

            post_text = AIContentGenerator.generate_post_text(theme)
            print(f"Текст поста: {post_text}")

            await self.application.bot.send_message(
                chat_id=Config.CHANNEL_ID, text=post_text
            )

            print(f"✅ Авто-пост отправлен в {time.strftime('%H:%M:%S')}")

        except Exception as e:
            print(f"❌ Ошибка авто-постинга: {e}")

    async def post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔄 Создаю пост...")

        try:
            from ai_generator import AIContentGenerator

            theme = random.choice(Config.THEMES)
            print(f"Генерирую пост на тему: {theme}")

            post_text = AIContentGenerator.generate_post_text(theme)
            print(f"Текст поста: {post_text}")

            await self.application.bot.send_message(
                chat_id=Config.CHANNEL_ID, text=post_text
            )

            await update.message.reply_text("✅ AI пост отправлен!")

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            await update.message.reply_text(f"❌ Ошибка: {e}")

    async def start_auto_posting(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Запуск автоматического постинга"""
        if self.auto_posting:
            await update.message.reply_text("⚠️ Авто-постинг уже запущен!")
            return

        self.auto_posting = True

        # Запускаем планировщик в отдельном потоке
        def run_scheduler():
            asyncio.run(self._scheduler_loop())

        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()

        await update.message.reply_text(
            f"🚀 Авто-постинг запущен!\n"
            f"📅 Интервал: {Config.POST_INTERVAL} часов\n"
            f"⏰ Следующий пост через {Config.POST_INTERVAL} часов\n"
            f"📊 Канал: {Config.CHANNEL_ID}"
        )

        print(f"✅ Авто-постинг запущен с интервалом {Config.POST_INTERVAL} часов")

    async def _scheduler_loop(self):
        """Цикл планировщика"""
        while self.auto_posting:
            await self.create_auto_post()
            await asyncio.sleep(Config.POST_INTERVAL * 3600)  # Ждем N часов

    async def stop_auto_posting(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Остановка автоматического постинга"""
        if not self.auto_posting:
            await update.message.reply_text("⚠️ Авто-постинг не был запущен!")
            return

        self.auto_posting = False

        await update.message.reply_text("🛑 Авто-постинг остановлен!")
        print("✅ Авто-постинг остановлен")

    async def test(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🧪 Тестирую генерацию...")

        try:
            from ai_generator import AIContentGenerator

            theme = random.choice(Config.THEMES)
            post_text = AIContentGenerator.generate_post_text(theme)

            await update.message.reply_text(f"📝 Тема: {theme}\n\n{post_text}")

        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {e}")

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("post", self.post))
        self.application.add_handler(
            CommandHandler("start_auto", self.start_auto_posting)
        )
        self.application.add_handler(
            CommandHandler("stop_auto", self.stop_auto_posting)
        )
        self.application.add_handler(CommandHandler("test", self.test))

    def run(self):
        print("=== ЗАПУСК БОТА ===")
        print(f"Токен: {Config.BOT_TOKEN[:10]}...")
        print(f"Канал: {Config.CHANNEL_ID}")
        print(f"Интервал авто-постинга: {Config.POST_INTERVAL} часов")

        self.setup_handlers()
        print("🤖 Бот запускается...")

        print("🔄 Запуск polling...")
        print("💡 Доступные команды:")
        print("   /start - информация о боте")
        print("   /post - создать пост")
        print("   /start_auto - запустить авто-постинг")
        print("   /stop_auto - остановить авто-постинг")
        print("   /test - тест генерации")
        print("⏹️  Нажмите Ctrl+C для остановки")

        # Запускаем бота
        self.application.run_polling()


if __name__ == "__main__":
    print("🔧 ТОЧКА ВХОДА")
    bot = AIPosterBot()
    bot.run()
