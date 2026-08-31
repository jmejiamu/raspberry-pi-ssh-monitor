import json
import time

from parser import parse_ssh_failed_login
from detector import detect_threat
from display import show_banner, show_status, show_event, show_alert


LOG_FILE = "/var/log/auth.log"
EVENT_FILE = "security_events.jsonl"


def save_event(event):
    with open(EVENT_FILE, "a") as file:
        file.write(json.dumps(event) + "\n")


with open(LOG_FILE, "r") as file:
    file.seek(0, 2)

    show_banner()
    show_status(LOG_FILE)

    while True:
        line = file.readline()

        if not line:
            time.sleep(0.5)
            continue

        parsed_event = parse_ssh_failed_login(line)

        if parsed_event is None:
            continue

        detection = detect_threat(parsed_event)

        show_event(detection)

        if detection["severity"] == "high":
            show_alert(detection)

        save_event(detection)