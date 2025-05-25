import subprocess
import time
import re
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText

# --- Configuration ---
THRESHOLD = 3
TIME_WINDOW = 60  # seconds
EMAIL_ALERTS = True
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "abinash.yad4v@gmail.com"
EMAIL_PASSWORD = "dsyy asho ddyw niyj"  # Use an app-specific password
EMAIL_RECEIVER = "abinash.yad4v@gmail.com"

# --- Failed login pattern ---
FAIL_PATTERN = re.compile(r"Failed password for(?: invalid user)? (\w+) from ([\d.:]+)")

# --- Track failed attempts ---
fail_log = defaultdict(list)

def send_email_alert(ip, count):
    subject = f"[ALERT] SSH Brute-force Attempt Detected from {ip}"
    body = f"Detected {count} failed SSH login attempts from IP: {ip} within {TIME_WINDOW} seconds."

    msg = MIMEText(body)
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"[!] Email alert sent for IP: {ip}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

def monitor_ssh_logs():
    print("[*] Monitoring SSH failures from journalctl...")
    journal = subprocess.Popen(
        ["journalctl", "-fu", "ssh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for line in iter(journal.stdout.readline, ""):
        print(f"LOG: {line.strip()}")  # Optional: Keep this line for debugging
        match = FAIL_PATTERN.search(line)
        if match:
            user, ip = match.groups()

            # Skip localhost IPs to avoid false alerts
            if ip == '::1' or ip == '127.0.0.1':
                continue

            now = time.time()
            fail_log[ip].append(now)
            # Remove old timestamps outside the time window
            fail_log[ip] = [t for t in fail_log[ip] if now - t <= TIME_WINDOW]

            if len(fail_log[ip]) >= THRESHOLD:
                print(f"[!] Alert: {len(fail_log[ip])} failures from {ip}")
                if EMAIL_ALERTS:
                    send_email_alert(ip, len(fail_log[ip]))
                fail_log[ip] = []  # Reset to avoid duplicate alerts

try:
    monitor_ssh_logs()
except KeyboardInterrupt:
    print("[+] Monitoring stopped by user.")
