"""Notification services: Email and Telegram."""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Send notifications via Telegram bot."""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = bool(bot_token and chat_id)

    def send(self, message: str) -> bool:
        if not self.enabled:
            return False
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            resp = requests.post(url, json={"chat_id": self.chat_id, "text": message}, timeout=10)
            resp.raise_for_status()
            logger.info("Telegram notification sent.")
            return True
        except Exception as e:
            logger.warning("Telegram error: %s", e)
            return False


class EmailNotifier:
    """Send notifications via SMTP email."""

    def __init__(self, enabled: bool, sender: str, to: str, password: str,
                 smtp_server: str = "smtp.gmail.com", smtp_port: int = 465):
        self.enabled = enabled and bool(sender and to and password)
        self.sender = sender
        self.to = to
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send(self, subject: str, body: str) -> bool:
        if not self.enabled:
            return False
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = self.to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            if self.smtp_port == 465:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.sender, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender, self.password)
                    server.send_message(msg)

            logger.info("Email sent to %s", self.to)
            return True
        except Exception as e:
            logger.warning("Email error: %s", e)
            return False
