import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests


TIMEZONE = "America/Vancouver"
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]


def get_next_registration_period():
    now = datetime.now(ZoneInfo(TIMEZONE))

    # Python weekday:
    # Monday = 0 ... Sunday = 6
    days_until_sunday = (6 - now.weekday()) % 7

    # 如果今天已经是周日～周六，
    # 我们需要找“下一周”的周日。
    if days_until_sunday == 0:
        days_until_sunday = 7

    start = (now + timedelta(days=days_until_sunday)).date()
    end = start + timedelta(days=6)

    return start, end


def format_date(date):
    return date.strftime("%b %-d")


def send_discord_message():
    start, end = get_next_registration_period()

    title = f"📝 这周的报名表（{format_date(start)} - {format_date(end)}）"

    # ====== 你以后主要修改这里 ======
    description = (
        "请大家填写下周的报名表。\n\n"
        "谢谢大家！"
    )
    # =================================

    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": 5814783,
            }
        ]
    }

    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    print(f"Discord message sent successfully: {title}")


if __name__ == "__main__":
    send_discord_message()
