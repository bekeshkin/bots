# AGENTS.md

## Project

`ebbot` is a small Python Telegram bot. It replies in Telegram when users mention `@ebbot` and asks OpenAI for a short Russian explanation.

## Files

- `bot.py` - main bot code.
- `requirements.txt` - Python dependencies.
- `README.md` - user-facing usage and setup docs.

## Bot Behavior

Keep these rules intact unless the user explicitly asks to change them:

- Direct message with `@ebbot <phrase>`: explain `<phrase>` only if it is 1 to 5 words.
- Direct message with only `@ebbot`: reply `What I need explain?`.
- Reply to another Telegram message with only `@ebbot`: explain the replied message text or caption.
- Reply mode does not check the 5-word limit.
- Token/quota/rate-limit OpenAI errors reply with `Tokens are over. Please ebbot tomorrow.`.

## Prompts

Direct short phrase prompt:

```text
Объясни простыми словами, что такое: <text>. Не больше 50 слов.
```

Reply-only prompt:

```text
Поясни <text post>. Не более 50 слов.
```

## Setup

Use environment variables for secrets. Do not hardcode tokens.

Required:

- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`

Optional:

- `BOT_NAME`, default `@ebbot`
- `OPENAI_MODEL`, default `gpt-4o-mini`
- `OPENAI_BASE_URL`, default `https://api.openai.com/v1`

## Development Notes

- Keep the project simple; avoid adding frameworks unless needed.
- Prefer small, readable functions in `bot.py`.
- If changing bot behavior, update `README.md` too.
- This workspace may not have Python installed, so mention clearly if tests or syntax checks could not be run.
