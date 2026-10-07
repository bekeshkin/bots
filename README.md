# ebbot

Simple Telegram bot for short explanations in chat.

## How to use in Telegram

Write the bot name with a short phrase, up to 5 words:

```text
@ebbot стейблкоин
```

The bot detects the phrase language and answers in the same language, no more than 50 words.

Reply to any message and write only:

```text
@ebbot
```

The bot explains the message you replied to and answers in the same language as that message. In this mode the 5-word limit is not checked, because the text comes from the replied post.

If you write:

```text
@ebbot help
```

the bot returns usage instructions in English.

If you write only `@ebbot` without replying to a message, the bot answers:

```text
What I need explain?
```

If OpenAI tokens or quota are over, the bot answers:

```text
Tokens are over. Please ebbot tomorrow.
```

## Bot prompts

For a direct short phrase, the bot sends:

```text
Определи язык текста и ответь на том же языке. Поясни простыми словами: <text>. Не более 50 слов.
```

For a reply with only `@ebbot`, the bot sends:

```text
Определи язык текста и ответь на том же языке. Поясни этот пост: <text post>. Не более 50 слов.
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
$env:OPENAI_API_KEY = "your_openai_api_key"
python bot.py
```

Optional settings:

```powershell
$env:BOT_NAME = "@ebbot"
$env:OPENAI_MODEL = "gpt-4o-mini"
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"
```

