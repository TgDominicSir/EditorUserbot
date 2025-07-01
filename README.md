# Telegram UserBot Editor

A Heroku-ready Pyrogram userbot to edit bot links in messages and captions across multiple Telegram channels.

## Usage

Send this command to the bot:
```
/edit <chan1,chan2,...> <old_bot> <new_bot>
```

Example:
```
/edit -1001234567890,-1009876543210 abcdBot efghBot
```

## Setup on Heroku

Set these config vars:

- API_ID
- API_HASH
- SESSION_STRING
- ADMIN_ID (your Telegram numeric user ID)

Then deploy the bot.
