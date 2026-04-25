import datetime
import json

import httpx


def main() -> None:
    base = "http://127.0.0.1:8000"

    with httpx.Client(timeout=10.0) as client:
        profile = client.post(
            f"{base}/api/profiles",
            json={
                "parent_name": "重庆试点用户",
                "parent_phone": "13800000001",
                "child_name": "子女A",
                "child_phone": "13900000001",
                "chronic_diseases": "高血压",
                "allergies": "无",
                "mobility_limitations": "轻度",
                "interests": "culture,food",
                "wechat_webhook_url": "",
            },
        ).json()

        trip = client.post(
            f"{base}/api/trips",
            json={
                "profile_id": profile["id"],
                "destination": "洪崖洞",
                "travel_date": str(datetime.date.today()),
            },
        ).json()

        sos = client.post(
            f"{base}/api/sos/trigger",
            json={
                "profile_id": profile["id"],
                "trip_id": trip["id"],
                "latitude": 29.56301,
                "longitude": 106.55156,
                "network_status": "online",
            },
        ).json()

        task = client.post(
            f"{base}/api/tasks",
            json={
                "profile_id": profile["id"],
                "trip_id": trip["id"],
                "title": "拍一张最喜欢的江景",
                "description": "在江边拍照并上传",
            },
        ).json()

        client.post(
            f"{base}/api/tasks/{task['id']}/complete",
            json={"completed_note": "已完成", "photo_url": "https://example.com/chongqing.jpg"},
        ).json()

        feedback = client.post(
            f"{base}/api/tasks/{task['id']}/feedback",
            json={"feedback_text": "太棒了", "hearts_delta": 1},
        ).json()

        card = client.post(
            f"{base}/api/cards/generate",
            json={"trip_id": trip["id"], "title": "重庆试点数字卡片", "image_url": ""},
        ).json()

        guide = client.post(
            f"{base}/api/guide/ask",
            json={"question": "Tell me about Hongya Cave"},
        ).json()

    summary = {
        "profile_id": profile["id"],
        "trip_id": trip["id"],
        "task_id": task["id"],
        "card_id": card["id"],
        "sms_status": sos["sms_status"],
        "wechat_status": sos["wechat_status"],
        "task_hearts": feedback["hearts"],
        "guide_scope": guide["scope"],
        "guide_confidence": guide["confidence"],
    }

    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
