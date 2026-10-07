import logging
import os
import re

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


BOT_NAME = os.getenv("BOT_NAME", "@ebbot").lower()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TOKENS_OVER_MESSAGE = "Tokens are over. Please ebbot tomorrow."


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class TokensOverError(Exception):
    pass


def clean_trigger_text(message_text: str) -> str:
    text = re.sub(re.escape(BOT_NAME), "", message_text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,:;.!?\n\t")


def is_short_phrase(text: str) -> bool:
    return 0 < len(text.split()) <= 5


def is_tokens_over_response(response: requests.Response) -> bool:
    if response.status_code == 429:
        return True

    try:
        error = response.json().get("error", {})
    except ValueError:
        return False

    code = error.get("code", "")
    message = error.get("message", "").lower()
    return code in {
        "insufficient_quota",
        "rate_limit_exceeded",
        "billing_hard_limit_reached",
    } or "quota" in message or "rate limit" in message


def ask_openai(text: str, explain_post: bool = False) -> str:
    if explain_post:
        prompt = f"Поясни {text}. Не более 50 слов."
    else:
        prompt = f"Объясни простыми словами, что такое: {text}. Не больше 50 слов."

    response = requests.post(
        f"{OPENAI_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 90,
        },
        timeout=30,
    )

    if is_tokens_over_response(response):
        raise TokensOverError

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Send a short phrase with {BOT_NAME}, or reply to a post and mention {BOT_NAME}."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message or not message.text:
        return

    message_text = message.text.strip()
    if BOT_NAME not in message_text.lower():
        return

    phrase = clean_trigger_text(message_text)
    explain_post = False
    if message.reply_to_message:
        explain_post = not phrase
        replied = message.reply_to_message.text or message.reply_to_message.caption or ""
        phrase = replied.strip()
    elif not phrase:
        await message.reply_text("What I need explain?")
        return
    elif not is_short_phrase(phrase):
        return

    try:
        answer = ask_openai(phrase, explain_post=explain_post)
    except TokensOverError:
        await message.reply_text(TOKENS_OVER_MESSAGE)
        return
    except requests.RequestException:
        logger.exception("OpenAI request failed")
        await message.reply_text("Sorry, I could not get an answer now.")
        return

    await message.reply_text(answer)


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN before starting the bot.")
    if not OPENAI_API_KEY:
        raise RuntimeError("Set OPENAI_API_KEY before starting the bot.")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
