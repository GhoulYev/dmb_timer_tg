"""
Inline-бот: обратный отсчёт до 27 октября 2027 + процент пути от 28 апреля 2026.

Запуск:  pip install -r requirements.txt && python bot.py
Токен берётся из переменной окружения BOT_TOKEN или из файла .env
Опционально: TZ_NAME=Europe/Moscow (часовой пояс для дат)
"""
import os
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, ContextTypes, InlineQueryHandler

load_dotenv()

TZ = ZoneInfo(os.getenv("TZ_NAME", "Europe/Moscow"))
START = datetime(2026, 4, 28, tzinfo=TZ)
END = datetime(2027, 10, 27, tzinfo=TZ)


def build_text() -> str:
    now = datetime.now(TZ)
    left = max((END - now).total_seconds(), 0)
    total = (END - START).total_seconds()
    passed = min(max((now - START).total_seconds(), 0), total)
    percent = passed / total * 100

    secs = int(left)
    days, rem = divmod(secs, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    return (
        "⏳ До 27 октября 2027:\n"
        f"{days} дн. {hours} ч. {minutes} мин. {seconds} сек.\n\n"
        f"📊 Пройдено с 28 апреля 2026: {percent:.4f}%"
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = build_text()
    result = InlineQueryResultArticle(
        id=str(uuid4()),
        title="Сколько осталось до 27.10.2027",
        description="Нажми, чтобы отправить в чат",
        input_message_content=InputTextMessageContent(text),
    )
    await update.inline_query.answer([result], cache_time=0, is_personal=True)


def main() -> None:
    app = Application.builder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(InlineQueryHandler(inline_query))
    app.run_polling(allowed_updates=["inline_query"])


if __name__ == "__main__":
    main()
