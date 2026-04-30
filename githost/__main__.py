"""Entry point for running GitHost Pro standalone."""

import logging
import sys
import threading

from .config import AppConfig
from .storage import GitHubStorage
from .notifications import EmailNotifier, TelegramNotifier
from .shortener import BitlyShortener
from .cleanup import cleanup_expired
from .app import create_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("githost")


def run():
    """Run GitHost Pro."""
    config = AppConfig.from_env()

    if not config.github.token:
        logger.error("GITHUB_TOKEN is required.")
        sys.exit(1)
    if not config.ngrok.auth_token:
        logger.warning("NGROK_AUTH_TOKEN not set — public URL will not be available.")

    # Setup storage
    storage = GitHubStorage(
        username=config.github.username,
        token=config.github.token,
        repo_name=config.github.repo_name,
    )
    storage.setup()

    # Cleanup expired
    removed = cleanup_expired(storage.links_db, storage.media_dir, storage.thumbs_dir)
    if removed:
        storage.save_links_db()

    # Setup notifiers
    email_notifier = EmailNotifier(
        enabled=config.email.enabled,
        sender=config.email.sender,
        to=config.email.to,
        password=config.email.password,
        smtp_server=config.email.smtp_server,
        smtp_port=config.email.smtp_port,
    )
    telegram_notifier = TelegramNotifier(
        bot_token=config.telegram.bot_token,
        chat_id=config.telegram.chat_id,
    )
    shortener = BitlyShortener(config.bitly.access_token)

    # Create app
    app = create_app(
        storage=storage,
        config=config,
        notifier_email=email_notifier,
        notifier_telegram=telegram_notifier,
        shortener=shortener,
    )

    # Start Flask
    logger.info("Starting GitHost Pro on %s:%d", config.server.host, config.server.port)
    app.run(host=config.server.host, port=config.server.port, debug=False)


if __name__ == "__main__":
    run()
