#..........This Bot Made By [RAHAT](https://t.me/r4h4t_69)..........#
#..........Anyone Can Modify This As He Likes..........#
#..........Just one requests do not remove my credit..........#

import os
import json

def _parse_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default

def _parse_int_list(env_value: str) -> list[int]:
    """
    Accepts:
      - JSON list string: "[-100111,-100222]"
      - Comma-separated: "-100111,-100222"
      - Single value: "-100111"
    Returns: list[int]
    """
    if not env_value:
        return []
    env_value = env_value.strip()
    # Try JSON first
    try:
        parsed = json.loads(env_value)
        if isinstance(parsed, list):
            return [_parse_int(str(x)) for x in parsed]
        # single int inside JSON
        return [_parse_int(str(parsed))]
    except Exception:
        # fallback: comma-separated
        parts = [p for p in env_value.replace(" ", "").split(",") if p]
        return [_parse_int(p) for p in parts]

def _parse_str_list(env_value: str, default: list[str] | None = None) -> list[str]:
    if not env_value:
        return default or []
    # allow JSON array or comma separated
    try:
        parsed = json.loads(env_value)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass
    return [s.strip() for s in env_value.split(",") if s.strip()]

API_ID = _parse_int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

MONGO_URL = os.getenv("MONGO_URL", "")
DB_NAME = os.getenv("DB_NAME", "Rahat")

# Images: JSON array or comma-separated
START_PIC = _parse_str_list(
    os.getenv("START_PICS", ""),
    default=["https://envs.sh/aWO.jpg"]
)

# Two (or more) log channels supported
# Example: LOG_CHANNELS="-1001111111111,-1002222222222"
LOG_CHANNELS = _parse_int_list(os.getenv("LOG_CHANNELS", "-1002477079513"))

# Back-compat (if someone still sets a single LOG_CHANNEL)
_single = os.getenv("LOG_CHANNEL", "")
if _single and not LOG_CHANNELS:
    LOG_CHANNELS = [_parse_int(_single)]

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

# Admins: JSON array or comma-separated of user IDs
ADMIN = _parse_int_list(os.getenv("ADMIN", "")) or []

