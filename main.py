from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import re, asyncio
from config import API_ID, API_HASH, SESSION_STRING, ADMIN_ID

app = Client(
    "userbot",
    session_string=SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH,
    sleep_threshold=10
)

@app.on_message(filters.command("edit") & filters.user(int(ADMIN_ID)))
async def edit_links(client, message):
    args = message.text.split(maxsplit=3)
    if len(args) != 4:
        return await safe_reply(message, "Usage:\n`/edit <chan1,chan2> <old_bot> <new_bot>`")

    channel_ids = args[1].split(",")
    old_bot = args[2]
    new_bot = args[3]

    pattern = re.compile(rf"https://t\.me/{old_bot}\?start=([\w-]+)")
    total_edited = 0

    for chan_id in channel_ids:
        try:
            chan_id = int(chan_id.strip())
            edited_count = 0

            async for msg in client.get_chat_history(chan_id, limit=500):
                text = msg.text or msg.caption
                if not text or old_bot not in text:
                    continue

                new_text = re.sub(
                    rf"https://t\.me/{old_bot}\?start=([\w-]+)",
                    rf"https://t.me/{new_bot}?start=\1",
                    text
                )

                if new_text != text:
                    try:
                        if msg.text:
                            await msg.edit_text(new_text)
                        else:
                            await msg.edit_caption(new_text)
                        edited_count += 1
                        await asyncio.sleep(1)  # Avoid bulk edit penalty
                    except FloodWait as fw:
                        print(f"FloodWait: Sleeping for {fw.value} sec")
                        await asyncio.sleep(fw.value)
                    except Exception as e:
                        print(f"Edit failed: {e}")

            total_edited += edited_count
            await safe_reply(message, f"✅ {edited_count} messages edited in {chan_id}")
            await asyncio.sleep(5)  # Cooldown after each channel

        except Exception as e:
            await safe_reply(message, f"❌ Failed for {chan_id}: {e}")
            await asyncio.sleep(2)

    await safe_reply(message, f"✅ Total edited across all channels: {total_edited}")


async def safe_reply(message, text):
    """Helper to safely reply without flood crash."""
    try:
        await message.reply(text)
    except FloodWait as fw:
        print(f"Reply FloodWait: Sleeping for {fw.value} sec")
        await asyncio.sleep(fw.value)
        await message.reply(text)
    except Exception as e:
        print(f"Reply failed: {e}")


app.run()
