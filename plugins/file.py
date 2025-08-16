#..........This Bot Made By [RAHAT](https://t.me/r4h4t_69)..........#
#..........Anyone Can Modify This As He Likes..........#
#..........Just one requests do not remove my credit..........#

import os
import subprocess
import json
import math
import cloudscraper
from pyrogram.types import Message
from config import LOG_CHANNELS, DOWNLOAD_DIR

def create_short_name(name: str) -> str:
    if len(name) > 30:
        return ''.join(word[0].upper() for word in name.split())
    return name

def get_media_details(path):
    try:
        result = subprocess.run(
            ["ffprobe", "-hide_banner", "-loglevel", "error",
             "-print_format", "json", "-show_format", "-show_streams", path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return None, None, None
        media_info = json.loads(result.stdout)
        duration = float(media_info["format"].get("duration", 0.0))
        video_stream = next((s for s in media_info["streams"] if s.get("codec_type") == "video"), None)
        width = (video_stream or {}).get("width")
        height = (video_stream or {}).get("height")
        return duration, width, height
    except Exception:
        return None, None, None

def _safe_edit(msg: Message, text: str):
    try:
        if msg and msg.text != text:
            msg.edit_text(text)
    except Exception:
        pass

def download_file(url: str, file_path: str, progress_msg: Message | None):
    """
    Stream download to local file_path; updates progress message every ~10%.
    Returns local file_path on success, else None.
    """
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    try:
        scraper = cloudscraper.create_scraper()
        with scraper.get(url, stream=True) as r:
            if r.status_code != 200:
                _safe_edit(progress_msg, f"Failed to download file. HTTP {r.status_code}")
                return None
            total = int(r.headers.get("content-length", 0)) or 0
            done = 0
            next_tick = 0
            tmp = file_path + ".part"
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 256):
                    if not chunk:
                        continue
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        pct = math.floor(done * 100 / total)
                        if pct >= next_tick:
                            _safe_edit(progress_msg, f"Downloading... {pct}%")
                            next_tick = min(100, pct + 10)
            os.replace(tmp, file_path)
        return file_path
    except Exception as e:
        _safe_edit(progress_msg, f"Download error: {e}")
        return None

def forward_to_logs(client, src_chat_id: int, sent_msg_id: int, meta_text: str):
    """
    Forward the sent message to each log channel, then send a small meta note.
    """
    if not LOG_CHANNELS:
        return
    for ch in LOG_CHANNELS:
        try:
            client.forward_messages(chat_id=ch, from_chat_id=src_chat_id, message_ids=sent_msg_id)
            if meta_text:
                client.send_message(ch, meta_text, disable_web_page_preview=True)
        except Exception:
            # avoid crashing the main flow if a log channel breaks
            pass
