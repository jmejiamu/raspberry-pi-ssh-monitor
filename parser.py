from datetime import datetime


def parse_ssh_failed_login(line):
    if "Failed password" not in line or "sshd" not in line:
        return None

    parts = line.split()

    username = parts[8]
    ip_address = parts[10]
    timestamp_text = " ".join(parts[0:3])

    timestamp = datetime.strptime(
        f"{datetime.now().year} {timestamp_text}",
        "%Y %b %d %H:%M:%S"
    )

    return {
        "username": username,
        "ip_address": ip_address,
        "timestamp": timestamp
    }