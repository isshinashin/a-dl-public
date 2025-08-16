Perfect 👍 thanks for pasting the full file.

Right now your code tries to send one message to `LOG_CHANNELS` as if it’s a single ID, but it’s actually a list.
We’ll fix that by looping over all channels in `LOG_CHANNELS`.

Here’s the **fixed full code** 👇

```python
#..........This Bot Made By [RAHAT](https://t.me/r4h4t_69)..........#
#..........Anyone Can Modify This As He Likes..........#
#..........Just one request: do not remove my credit..........#

# --- Keep-alive server for Koyeb ---
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!", 200

def run_server():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_server, daemon=True).start()
# --- End keep-alive section ---

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNELS
import logging
import os
import shutil
from pyrogram.errors import PeerIdInvalid, ChatAdminRequired

logging.basicConfig(level=logging.INFO)

# Create the downloads directory if it doesn't exist
if os.path.exists("./downloads"):
    shutil.rmtree("./downloads")
os.makedirs("./downloads")


class AnimePaheBot(Client):
    def __init__(self):
        super().__init__(
            "AnimePaheBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            sleep_threshold=120,
        )

    async def start(self):
        await super().start()
        print("✅ Bot Started")

        # Test log channel access
        if isinstance(LOG_CHANNELS, (list, tuple)):
            for channel in LOG_CHANNELS:
                try:
                    await self.send_message(channel, "✅ Bot is connected to the log channel and ready.")
                    print(f"✅ Successfully sent test message to LOG_CHANNEL ({channel})")
                except PeerIdInvalid:
                    print(f"❌ ERROR: LOG_CHANNEL ID {channel} is invalid. Please check with @userinfobot.")
                except ChatAdminRequired:
                    print(f"❌ ERROR: Bot is not an admin in LOG_CHANNEL ({channel}). Please add it as admin.")
                except Exception as e:
                    print(f"❌ ERROR: Could not send message to LOG_CHANNEL ({channel}) — {e}")
        else:
            try:
                await self.send_message(LOG_CHANNELS, "✅ Bot is connected to the log channel and ready.")
                print(f"✅ Successfully sent test message to LOG_CHANNELS ({LOG_CHANNELS})")
            except PeerIdInvalid:
                print(f"❌ ERROR: LOG_CHANNELS ID {LOG_CHANNELS} is invalid. Please check with @userinfobot.")
            except ChatAdminRequired:
                print(f"❌ ERROR: Bot is not an admin in LOG_CHANNELS ({LOG_CHANNELS}). Please add it as admin.")
            except Exception as e:
                print(f"❌ ERROR: Could not send message to LOG_CHANNELS ({LOG_CHANNELS}) — {e}")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped")


if __name__ == "__main__":
    app_bot = AnimePaheBot()
    app_bot.run()

