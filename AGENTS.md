# AGENTS.md

## Project

`ebbot` is a small Python Telegram bot. It replies in Telegram when users mention `@ebbot` and asks OpenRouter for a short explanation in the same language as the source text.

## Files

- `bot.py` - main bot code.
- `requirements.txt` - Python dependencies.
- `README.md` - user-facing usage and setup docs.

## Bot Behavior

Keep these rules intact unless the user explicitly asks to change them:

- Direct message with `@ebbot <phrase>`: explain `<phrase>` only if it is 1 to 5 words.
- Direct message with only `@ebbot`: reply `What I need explain?`.
- Direct message with `@ebbot help`: return usage instructions in English without calling OpenRouter.
- Reply to another Telegram message with only `@ebbot`: explain the replied message text or caption.
- Reply mode does not check the 5-word limit.
- Answers should use the same language as the phrase or replied post.
- Token/quota/credits/rate-limit OpenRouter errors reply with `Tokens are over. Please ebbot tomorrow.`.

## OpenRouter

Default model:

```text
openrouter/free
```

Default base URL:

```text
https://openrouter.ai/api/v1
```

## Prompts

Direct short phrase prompt:

```text
Определи язык текста и ответь на том же языке. Поясни простыми словами: <text>. Не более 50 слов.
```

Reply-only prompt:

```text
Определи язык текста и ответь на том же языке. Поясни этот пост: <text post>. Не более 50 слов.
```

## Setup

Use environment variables for secrets. Do not hardcode tokens.

Required:

- `TELEGRAM_BOT_TOKEN`
- `OPENROUTER_API_KEY`

Optional:

- `BOT_NAME`, default `@ebbot`
- `OPENROUTER_MODEL`, default `openrouter/free`
- `OPENROUTER_BASE_URL`, default `https://openrouter.ai/api/v1`
- `OPENROUTER_SITE_NAME`, default `ebbot`
- `OPENROUTER_SITE_URL`

## Development Notes

- Keep the project simple; avoid adding frameworks unless needed.
- Prefer small, readable functions in `bot.py`.
- If changing bot behavior, update `README.md` too.
- This workspace may not have Python installed, so mention clearly if tests or syntax checks could not be run.
