#..........This Bot Made By [RAHAT](https://t.me/r4h4t_69)..........#
#..........Anyone Can Modify This As He Likes..........#
#..........Just one requests do not remove my credit..........#

import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "Rahat")
START_PIC = os.getenv("START_PIC", "https://envs.sh/aWO.jpg").split(",")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", ""))
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

# ADMIN should be a comma-separated string in env, e.g. "5424565785,6443423376"
ADMIN = list(map(int, os.getenv("ADMIN", "").split(","))) if os.getenv("ADMIN") else []


START_PIC = os.environ.get("START_PIC", "https://graph.org/file/dfd1842d8a2dcc536a2b7.jpg https://graph.org/file/b55f0baaa7a6fde7c5682.jpg https://graph.org/file/3298ca8910c82f33418a8.jpg https://graph.org/file/4e4935469a7214c734721.jpg https://graph.org/file/fa5f2b241fe77beff8ba0.jpg https://graph.org/file/bcb9969f78ab4a47a483c.jpg https://graph.org/file/a9af161696d82f17b8888.jpg https://graph.org/file/d23b00650c00ce4d9a467.jpg https://graph.org/file/4dc0b3dfaad61fbcf0a49.jpg https://graph.org/file/7088315e9b0b6a2fa7118.jpg https://graph.org/file/9c9911d06e5f2316febb9.jpg https://graph.org/file/d2ee185180469cfd28071.jpg https://graph.org/file/dea04b2d615406aeb0181.jpg https://graph.org/file/98b63d3bb84984a68cc76.jpg").split()
