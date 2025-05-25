# SSH Log Monitor with Email Alerts

This Python script monitors SSH login failures in real-time using `journalctl`. It detects brute-force attacks by tracking multiple failed login attempts from the same IP address within a configurable time window and sends email alerts when a threshold is exceeded.

---

## Features

- Real-time monitoring of SSH failures using `journalctl`.
- Configurable threshold and time window for detecting brute-force attempts.
- Sends email alerts via SMTP (supports Gmail SMTP).
- Ignores localhost IPs to avoid false positives.
- Easy to configure with your email credentials.

---

## Requirements

- Python 3.x
- Access to `journalctl` on a system running `systemd` (e.g., most modern Linux distributions)
- An SMTP email account (Gmail recommended with App Password)

---

## Installation

1. Clone this repository or download the script:

	git clone https://github.com/abhinash-404/ssh-log-email-alert.git
	cd ssh-log-monitor

2. (Optional) Create a virtual environment and activate it:
	
	python3 -m venv venv
	source venv/bin/activate

## Configuration

THRESHOLD = 3          # Number of failed attempts to trigger alert
TIME_WINDOW = 60       # Time window in seconds
EMAIL_ALERTS = True    # Enable/disable email alerts

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com" #change this
EMAIL_PASSWORD = "your_app_password"  # Use Gmail App Passwords, not regular password
EMAIL_RECEIVER = "receiver_email@gmail.com" #change this

--> Important: Use Gmail App Passwords for EMAIL_PASSWORD if you have 2FA enabled on your Google account.

## Usage

Run the script with:
	python3 ssh_log_monitor_email.py

## Notes

The script uses journalctl -fu ssh to follow SSH logs, so you need appropriate permissions to run it (usually run as root or with sudo).

Ensure your firewall or email provider does not block SMTP connections.

This is a simple prototype for learning and demonstration purposes. For production, consider additional features like logging, configuration files, IP blocking, etc.

## Author

Abinash Yadav

