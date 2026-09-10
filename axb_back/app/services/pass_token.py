"""通行码生成服务"""
import hashlib
import hmac
from datetime import datetime

import segno

from app.config import get_settings

settings = get_settings()


def generate_pass_token(elder_id: int, trip_id: int) -> str:
    """生成动态通行码

    格式: ELDER-{elder_id}-{trip_id}-{timestamp_hash}
    """
    timestamp = datetime.utcnow().isoformat()
    message = f"{elder_id}:{trip_id}:{timestamp}"

    # 使用HMAC生成安全的哈希
    signature = hmac.new(
        settings.token_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()[:12]

    return f"ELDER-{elder_id}-{trip_id}-{signature}"


def generate_qr_code(data: str) -> str:
    """生成二维码SVG"""
    qr = segno.make(data)
    return qr.svg_inline(scale=5)


def verify_pass_token(token: str) -> dict | None:
    """验证通行码（基础验证）"""
    try:
        parts = token.split('-')
        if len(parts) != 4 or parts[0] != "ELDER":
            return None

        return {
            "elder_id": int(parts[1]),
            "trip_id": int(parts[2]),
            "signature": parts[3]
        }
    except (ValueError, IndexError):
        return None
