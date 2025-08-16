#..........This Bot Made By [RAHAT](https://t.me/r4h4t_69)..........#
#..........Anyone Can Modify This As He Likes..........#
#..........Just one request: do not remove my credit...#

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified
from plugins.direct_link import get_direct_from_kwik
from plugins.file import download_file, forward_to_logs, get_media_details
from plugins.commands import user_queries
from helper.database import get_caption, get_thumbnail   # ✅ fixed here
from config import DOWNLOAD_DIR, LOG_CHANNELS   # LOG_CHANNELS should be a list in config
from bs4 import BeautifulSoup
import os
import re
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

episode_data = {}

# ===== Default headers =====
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36"
    )
}

# ===== TLS Adapter for handshake fix =====
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        try:
            ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        except Exception:
            pass
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session_tls = requests.Session()
session_tls.mount("https://", TLSAdapter())

# ========= ANIME DETAILS =========
@Client.on_callback_query(filters.regex(r"^anime_"))
def anime_details(client, callback_query):
    session_id = callback_query.data.split("anime_")[1]
    query = user_queries.get(callback_query.message.chat.id, "")
    search_url = f"https://animepahe.ru/api?m=search&q={query.replace(' ', '+')}"
    response = requests.get(search_url).json()
    anime = next((a for a in response["data"] if a['id'] == session_id), None)
    if not anime:
        callback_query.answer("Anime not found. Try again.", show_alert=True)
        return

    details_url = f"https://animepahe.ru/anime/{anime['session']}"
    page = session_tls.get(details_url, headers=headers).text
    soup = BeautifulSoup(page, "html.parser")

    episodes = soup.find_all("li", {"data-episode-number": True})

    # store state for this chat
    episode_data[callback_query.message.chat.id] = {
        "anime_title": anime['title'],
        "anime_session_id": session_id,
        "episodes": {e['data-episode-number']: e['data-session'] for e in episodes}
    }

    buttons = []
    for i in range(len(episodes), 0, -1):
        epnum = str(i)
        buttons.append([InlineKeyboardButton(f"Episode {epnum}", callback_data=f"episode_{epnum}")])

    buttons.append([InlineKeyboardButton("Back to Search", callback_data="search")])
    buttons.append([InlineKeyboardButton("Close", callback_data="close")])
    reply_markup = InlineKeyboardMarkup(buttons)

    try:
        client.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id,
            text=f"**Anime:** {anime['title']}\n\nSelect an episode to download:",
            reply_markup=reply_markup
        )
    except MessageNotModified:
        pass


# ========= EPISODE DETAILS =========
@Client.on_callback_query(filters.regex(r"^episode_"))
def episode_details(client, callback_query):
    ep_no = callback_query.data.split("episode_")[1]
    chat_id = callback_query.message.chat.id

    data = episode_data.get(chat_id)
    if not data:
        callback_query.answer("Error: Data not found. Please /search again.", show_alert=True)
        return

    anime_title = data["anime_title"]
    anime_session_id = data["anime_session_id"]
    episode_session = data["episodes"].get(ep_no)
    if not episode_session:
        callback_query.answer("Episode not found.", show_alert=True)
        return

    download_url = f"https://animepahe.ru/download/{episode_session}"
    page = session_tls.get(download_url, headers=headers).text
    soup = BeautifulSoup(page, "html.parser")

    download_links = soup.find_all("a", {"href": re.compile(r"https://kwik.cx/f/.+")})
    if not download_links:
        callback_query.answer("No download links found for this episode.", show_alert=True)
        return

    buttons = []
    for link in download_links:
        quality = link.get("title", "Unknown Quality")
        buttons.append([InlineKeyboardButton(
            f"Download {quality}",
            callback_data=f"download_{episode_session}__{quality}"
        )])

    buttons.append([InlineKeyboardButton("Back to Anime", callback_data=f"anime_{anime_session_id}")])
    buttons.append([InlineKeyboardButton("Close", callback_data="close")])

    try:
        client.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.id,
            text=f"**Anime:** {anime_title}\n**Episode:** {ep_no}\n\nSelect a download quality:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        pass


# ========= DOWNLOAD START =========
@Client.on_callback_query(filters.regex(r"^download_"))
def download_start(client, callback_query):
    chat_id = callback_query.message.chat.id
    msg = callback_query.message

    # restore state
    data = episode_data.get(chat_id)
    if not data:
        callback_query.answer("Error: Data not found. Please /search again.", show_alert=True)
        return

    anime_title = data["anime_title"]

    try:
        episode_session, quality = callback_query.data.split("download_")[1].split("__")
    except Exception:
        callback_query.answer("Bad download data.", show_alert=True)
        return

    # find kwik link
    download_url = f"https://animepahe.ru/download/{episode_session}"
    page = session_tls.get(download_url, headers=headers).text
    soup = BeautifulSoup(page, "html.parser")

    kwik_url = None
    for link in soup.find_all("a", {"href": re.compile(r"https://kwik.cx/f/.+")}):
        if link.get("title", "Unknown Quality") == quality:
            kwik_url = link["href"]
            break

    if not kwik_url:
        callback_query.answer("Download link not found.", show_alert=True)
        return

    try:
        msg.edit_text("Resolving link…")
    except Exception:
        pass

    direct_link = get_direct_from_kwik(kwik_url)
    if not direct_link:
        callback_query.answer("Failed to resolve direct link.", show_alert=True)
        return

    safe_title = anime_title.replace("/", "-").replace("\\", "-")
    file_name = f"{safe_title} - {quality}.mp4"
    local_path = os.path.join(DOWNLOAD_DIR, file_name)

    try:
        msg.edit_text("Starting download… 0%")
    except Exception:
        pass

    saved = download_file(direct_link, local_path, msg)
    if not saved or not os.path.exists(saved):
        callback_query.answer("Download failed.", show_alert=True)
        return

    duration, width, height = get_media_details(saved)
    user_id = msg.from_user.id
    username = (msg.from_user.username and f"@{msg.from_user.username}") or "—"

    try:
        thumb_id = get_thumbnail(user_id)   # ✅ fixed here
        base_caption = get_caption(user_id) or ""
        cap = f"{base_caption}\n\n{safe_title} [{quality}]".strip()

        sent = client.send_document(
            chat_id=chat_id,
            document=saved,
            caption=cap
        ) if not (width and height) else client.send_video(
            chat_id=chat_id,
            video=saved,
            duration=int(duration) if duration else None,
            width=width,
            height=height,
            caption=cap,
            thumb=thumb_id if thumb_id else None
        )

        meta = (
            "📥 Forwarded download\n"
            f"👤 User: {username}\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"🎞️ Title: {safe_title}\n"
            f"✨ Quality: {quality}\n"
            f"🔗 Source: https://animepahe.ru/download/{episode_session}"
        )

        for log_ch in LOG_CHANNELS:
            forward_to_logs(client, chat_id, sent.id, meta, log_ch)

        try:
            msg.edit_text("✅ Done.")
        except Exception:
            pass

    except Exception as e:
        try:
            msg.edit_text(f"Send failed: {e}")
        except Exception:
            pass

    try:
        os.remove(saved)
    except Exception:
        pass


# ========= CLOSE BUTTON =========
@Client.on_callback_query(filters.regex(r"^close"))
def close_button(client, callback_query):
    client.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=callback_query.message.id
    )
