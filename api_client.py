import json
import os
import urllib.request
import urllib.error

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")


def send_event(event):
    if not API_URL:
        print("[API ERROR] API_URL is missing")
        return False

    data = json.dumps(event).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            print(f"[API] Event sent successfully: HTTP {response.status}")
            return response.status == 201

    except urllib.error.HTTPError as error:
        print(f"[API ERROR] HTTP {error.code}")
        print(error.read().decode())
        return False

    except urllib.error.URLError as error:
        print(f"[API ERROR] Could not connect to API: {error}")
        return False