"""URL shortening via Bit.ly."""

import logging
import requests

logger = logging.getLogger(__name__)


class BitlyShortener:
    """Shorten URLs using the Bit.ly API."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.enabled = bool(access_token)

    def shorten(self, long_url: str) -> str:
        """Shorten a URL. Returns the original URL if shortening fails or is disabled."""
        if not self.enabled:
            return long_url
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            resp = requests.post(
                "https://api-ssl.bitly.com/v4/shorten",
                headers=headers,
                json={"long_url": long_url},
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json()["link"]
            logger.warning("Bit.ly returned %d: %s", resp.status_code, resp.text)
        except Exception as e:
            logger.warning("Bit.ly error: %s", e)
        return long_url
