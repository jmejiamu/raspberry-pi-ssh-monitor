import json
import os
import urllib.request
import urllib.error

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")


def send_event(event):
    if not API_URL:
        print("[API ERROR] API_URL is not configured")
        return False

    data = json.dumps(event).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status == 201

    except urllib.error.URLError as error:
        print(f"[API ERROR] Could not send event: {error}")
        return False