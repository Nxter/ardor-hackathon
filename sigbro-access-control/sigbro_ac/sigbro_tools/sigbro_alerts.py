# -*- coding: UTF-8 -*-

import os
import requests
import json

from .sigbro_logs import sigbroLogs

log = sigbroLogs()

def send_alert_to_telegram(message: str):
    """Send alarm to telegram bot"""
    bot_token = os.environ.get("TELEGRAM_TOKEN", "")
    bot_chat_id = os.environ.get("TELEGRAM_CHAT", 0)

    params = dict()
    params["chat_id"] = bot_chat_id
    params["text"] = message

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    result = requests.post(url=url, data=json.dumps(params), headers={"Content-Type": "application/json"})
    return result


