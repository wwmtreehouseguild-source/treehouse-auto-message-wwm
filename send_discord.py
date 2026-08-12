import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests


TIMEZONE = "America/Vancouver"
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

ROLE_ID = "1536281241488330802"

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdYXTzkP_eQK_upDdrZTIY2dGQWf9lIWIAXDN72smDfDzbRiQ/viewform?pli=1"


def get_next_registration_period():
    now = datetime.now(ZoneInfo(TIMEZONE))

    # Monday = 0 ... Sunday = 6
    days_until_next_sunday = (6 - now.weekday()) % 7

    # If today is Sunday, use the following Sunday.
    if days_until_next_sunday == 0:
        days_until_next_sunday = 7

    start = (now + timedelta(days=days_until_next_sunday)).date()
    end = start + timedelta(days=6)

    return start, end


def format_date(date):
    return date.strftime("%b %-d")


def send_discord_message():
    start, end = get_next_registration_period()

    period = f"{format_date(start)} - {format_date(end)}"

    title = f"这是下周的报名表 - {period}"

    description = (
        f"<@&{ROLE_ID}> 请大家积极填写下周报名表："
        f"[点击这里填写报名表]({FORM_URL})"
        "\n\n"
        "谢谢大家的配合\n\n"
        "- 燕云Treehouse 管理组"
    )

    payload = {
        "content": f"<@&{ROLE_ID}>",
        "embeds": [
            {
                "title": title,
                "description": description,
            }
        ],
        "allowed_mentions": {
            "roles": [ROLE_ID]
        },
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
