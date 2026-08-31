# ANSI terminal colors
RESET = "\033[0m"
BOLD = "\033[1m"

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"


def show_banner():
    print(CYAN + r"""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║              SSH INTRUSION MONITOR                   ║
║                                                      ║
║              Raspberry Pi Security Lab               ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
""" + RESET)


def show_status(log_file):
    print(f"{BOLD} SYSTEM{RESET}")
    print(GRAY + " ─────────────────────────────────────────────────────" + RESET)

    print(f" Monitor       {GREEN}● ONLINE{RESET}")
    print(f" Log Source    {log_file}")
    print(" Rule          SSH_BRUTE_FORCE")
    print(" Threshold     5 attempts / 60 seconds")

    print(f"\n {CYAN}[*]{RESET} Waiting for authentication events...\n")


def show_event(event):
    severity = event["severity"].upper()

    if severity == "HIGH":
        severity_display = RED + severity + RESET
    elif severity == "MEDIUM":
        severity_display = YELLOW + severity + RESET
    else:
        severity_display = GREEN + severity + RESET

    print(" ┌─ SECURITY EVENT ───────────────────────────────────┐")
    print(" │                                                    │")
    print(f" │  Type       {event['type']:<37}│")
    print(f" │  Source IP  {event['ip_address']:<37}│")
    print(f" │  User       {event['username']:<37}│")
    print(f" │  Attempts   {event['attempt_count']:<37}│")
    print(f" │  Severity   {severity_display}")
    print(" │                                                    │")
    print(" └────────────────────────────────────────────────────┘")
    print()


def show_alert(event):
    print(RED + BOLD)
    print(" ╔═ SECURITY ALERT ═══════════════════════════════════╗")
    print(" ║                                                    ║")
    print(" ║             POSSIBLE SSH BRUTE FORCE               ║")
    print(" ║                                                    ║")
    print(f" ║  Source       {event['ip_address']:<35}║")
    print(f" ║  User         {event['username']:<35}║")
    print(f" ║  Attempts     {event['attempt_count']:<35}║")
    print(" ║  Window       60 seconds                           ║")
    print(" ║  Severity     HIGH                                 ║")
    print(" ║                                                    ║")
    print(" ╚════════════════════════════════════════════════════╝")
    print(RESET)