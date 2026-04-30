"""Configuration management for GitHost Pro."""

import os
import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class GitHubConfig:
    username: str = ""
    token: str = ""
    repo_name: str = "my-image-hosting"


@dataclass
class LinkDefaults:
    expiry_days: int = 7
    max_views: int = 0  # 0 = unlimited


@dataclass
class EmailConfig:
    enabled: bool = False
    to: str = ""
    sender: str = ""
    password: str = ""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465


@dataclass
class TelegramConfig:
    bot_token: str = ""
    chat_id: str = ""


@dataclass
class BitlyConfig:
    access_token: str = ""


@dataclass
class NgrokConfig:
    auth_token: str = ""
    subdomain: str = ""


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 5000
    admin_password: str = "admin123"
    secret_key: str = ""


@dataclass
class AppConfig:
    """Root configuration for GitHost."""
    github: GitHubConfig = field(default_factory=GitHubConfig)
    links: LinkDefaults = field(default_factory=LinkDefaults)
    email: EmailConfig = field(default_factory=EmailConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    bitly: BitlyConfig = field(default_factory=BitlyConfig)
    ngrok: NgrokConfig = field(default_factory=NgrokConfig)
    server: ServerConfig = field(default_factory=ServerConfig)

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load config from environment variables."""
        return cls(
            github=GitHubConfig(
                username=os.getenv("GITHUB_USERNAME", ""),
                token=os.getenv("GITHUB_TOKEN", ""),
                repo_name=os.getenv("REPO_NAME", "my-image-hosting"),
            ),
            links=LinkDefaults(
                expiry_days=int(os.getenv("DEFAULT_EXPIRY_DAYS", "7")),
                max_views=int(os.getenv("DEFAULT_MAX_VIEWS", "0")),
            ),
            email=EmailConfig(
                enabled=os.getenv("SEND_EMAIL", "false").lower() == "true",
                to=os.getenv("EMAIL_TO", ""),
                sender=os.getenv("EMAIL_FROM", ""),
                password=os.getenv("EMAIL_PASSWORD", ""),
                smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                smtp_port=int(os.getenv("SMTP_PORT", "465")),
            ),
            telegram=TelegramConfig(
                bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
                chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
            ),
            bitly=BitlyConfig(
                access_token=os.getenv("BITLY_ACCESS_TOKEN", ""),
            ),
            ngrok=NgrokConfig(
                auth_token=os.getenv("NGROK_AUTH_TOKEN", ""),
                subdomain=os.getenv("NGROK_SUBDOMAIN", ""),
            ),
            server=ServerConfig(
                admin_password=os.getenv("ADMIN_PASSWORD", "admin123"),
                secret_key=os.getenv("SECRET_KEY", os.urandom(32).hex()),
            ),
        )

    @classmethod
    def from_file(cls, path: str) -> "AppConfig":
        """Load config from a JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        return cls(
            github=GitHubConfig(**data.get("github", {})),
            links=LinkDefaults(**data.get("links", {})),
            email=EmailConfig(**data.get("email", {})),
            telegram=TelegramConfig(**data.get("telegram", {})),
            bitly=BitlyConfig(**data.get("bitly", {})),
            ngrok=NgrokConfig(**data.get("ngrok", {})),
            server=ServerConfig(**data.get("server", {})),
        )

    def to_file(self, path: str) -> None:
        """Save config to a JSON file."""
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)
