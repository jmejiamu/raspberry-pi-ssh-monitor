import json
import time
from collections import defaultdict
from datetime import datetime, timedelta

LOG_FILE = "/var/log/auth.log"
EVENT_FILE = "security_events.jsonl"

failed_attempts = defaultdict(list)

def save_event(event):
    with open(EVENT_FILE, "a") as file:
        file.write(json.dumps(event) + "\n")

def create_event(username, ip_address, attempt_count, timestamp):
    event = {
        "type": "ssh_failed_login",
        "severity": "medium",
        "username": username,
        "ip_address": ip_address,
        "attempt_count": attempt_count,
        "timestamp": timestamp.isoformat()
        }

    if attempt_count >= 5:
        event["type"] = "possible_brute_force"
        event["severity"] = "high"

    return event



with open(LOG_FILE, "r") as file:
    file.seek(0,2)
    
    print("SSH Monitor started...")
    print("Watching for failed SSH logins")
    print("Press Ctrl + C to stip.\n")

    while True:
        line = file.readline()
        
        if not line:
            time.sleep(0.5)
            continue

        if "Failed password" in line and "sshd" in line:
            part = line.split()


            username = part[8]
            ip_address = part[10]

            timestamp_text = " ".join(part[0:3])

            timestamp = datetime.strptime(
                f"{datetime.now().year} {timestamp_text}",
                "%Y %b %d %H:%M:%S"
                    )

            failed_attempts[ip_address].append(timestamp)

            one_minute_ago = timestamp - timedelta(seconds=60)

            failed_attempts[ip_address] = [
                    attempt
                    for attempt in failed_attempts[ip_address]
                    if attempt >= one_minute_ago
            ]

            attempt_count = len(failed_attempts[ip_address])

            event = create_event(
                username,
                ip_address,
                attempt_count,
                timestamp
            )

            print(json.dumps(event, indent=2))

            print("------------------------------------")

            save_event(event)
