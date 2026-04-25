from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass
class NotificationResult:
    sms_status: str
    wechat_status: str


async def _send_sms(phone: str, message: str, provider: str = "mock") -> str:
    if not phone:
        return "failed:no-phone"
    if provider == "mock":
        return "sent:mock"
    return "sent:provider"


async def _send_wechat(webhook_url: str, message: str) -> str:
    if not webhook_url:
        return "sent:mock"

    payload = {
        "msgtype": "text",
        "text": {"content": message},
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(webhook_url, json=payload)
        if response.status_code >= 400:
            return f"failed:{response.status_code}"
    except Exception:
        return "failed:network"
    return "sent:wechat"


async def send_dual_channel(
    child_phone: str,
    wechat_webhook_url: str,
    message: str,
    sms_provider: str,
) -> NotificationResult:
    sms_status = await _send_sms(child_phone, message, provider=sms_provider)
    wechat_status = await _send_wechat(wechat_webhook_url, message)
    return NotificationResult(sms_status=sms_status, wechat_status=wechat_status)
