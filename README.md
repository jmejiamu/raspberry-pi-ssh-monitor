# Raspberry Pi SSH Intrusion Monitor

A lightweight SSH security monitor for Raspberry Pi that analyzes Linux authentication logs in real time and detects potential brute-force login attempts.

## Features

- Live monitoring of `/var/log/auth.log`
- SSH failed-login detection
- Per-IP attempt tracking
- 60-second detection window
- Brute-force threat classification
- JSON event logging
- Security event forwarding to an external API
- Automatic startup with systemd

## Architecture

```text
Linux auth.log
      ↓
Python Parser
      ↓
Threat Detector
      ↓
Security Event
     ↙     ↘
JSON Log   REST API
```

## Detection Rule

An IP address is classified as a **possible brute-force attack** when it generates **5 or more failed SSH login attempts within 60 seconds**.

Detected events are classified as:

- `medium` — failed SSH login
- `high` — possible brute-force attack

## Project Structure

```text
ssh-monitor/
├── monitor.py       # Monitors authentication logs
├── parser.py        # Parses failed SSH login attempts
├── detector.py      # Applies detection rules
├── display.py       # Displays events and alerts
├── api_client.py    # Sends events to the API
└── tests/           # Parser and detector tests
```

## Setup

Create a `.env` file:

```env
API_URL=http://YOUR_API_IP:3001/api/events
```

Install dependencies:

```bash
pip3 install python-dotenv
```

## Run

```bash
sudo python3 monitor.py
```

The monitor can also be configured as a `systemd` service to start automatically when the Raspberry Pi boots.

## Related Repositories

This repository contains the Raspberry Pi detection agent for the SSH Intrusion Detection & Monitoring System.

- [Backend API](https://github.com/jmejiamu/ssh-intrusion-monitor-api) — TypeScript/Express API, MongoDB storage, and real-time Socket.io events.
- [Mobile Dashboard](https://github.com/jmejiamu/ssh-intrusion-monitor-app) — React Native dashboard for monitoring security events in real time.
