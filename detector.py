from collections import defaultdict
from datetime import timedelta


failed_attempts = defaultdict(list)
alerted_ips = set()


def detect_threat(event):
    ip_address = event["ip_address"]
    timestamp = event["timestamp"]

    failed_attempts[ip_address].append(timestamp)

    one_minute_ago = timestamp - timedelta(seconds=60)

    failed_attempts[ip_address] = [
        attempt
        for attempt in failed_attempts[ip_address]
        if attempt >= one_minute_ago
    ]

    attempt_count = len(failed_attempts[ip_address])

    detection = {
        "type": "ssh_failed_login",
        "severity": "medium",
        "username": event["username"],
        "ip_address": ip_address,
        "attempt_count": attempt_count,
        "timestamp": timestamp.isoformat(),
        "should_alert": False
    }

    if attempt_count >= 5:
        detection["type"] = "possible_brute_force"
        detection["severity"] = "high"

        if ip_address not in alerted_ips:
            detection["should_alert"] = True
            alerted_ips.add(ip_address)

    if attempt_count < 5:
        alerted_ips.discard(ip_address)

    return detection