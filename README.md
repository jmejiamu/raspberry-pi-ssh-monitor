# Raspberry Pi SSH Intrusion Monitor

A lightweight SSH security monitor for Raspberry Pi that watches Linux authentication logs and detects repeated failed SSH login attempts.

## Features

- Live monitoring of `/var/log/auth.log`
- SSH failed-login detection
- Per-IP tracking
- 60-second detection window
- Brute-force alerting
- JSON event logging

## Architecture

auth.log → parser → detector → security event

## Detection Rule

5 failed SSH login attempts from the same IP within 60 seconds triggers a high-severity possible brute-force alert.

## Run

```bash
sudo python3 monitor.py
```
