"""Automatic cleanup of expired links and files."""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def cleanup_expired(links_db: dict, media_dir: str, thumbs_dir: str) -> List[str]:
    """
    Remove expired links and their associated files.
    Returns list of removed link IDs.
    """
    now = datetime.now()
    to_delete = []

    for link_id, info in links_db.items():
        try:
            expiry = datetime.fromisoformat(info["expiry"])
            if now > expiry:
                to_delete.append(link_id)
        except (KeyError, ValueError) as e:
            logger.warning("Invalid link entry %s: %s", link_id, e)
            to_delete.append(link_id)

    for link_id in to_delete:
        info = links_db.pop(link_id, {})
        filename = info.get("filename", "")

        # Remove media file
        media_path = os.path.join(media_dir, filename)
        if os.path.exists(media_path):
            os.remove(media_path)
            logger.info("Removed expired file: %s", filename)

        # Remove thumbnail
        stem = Path(filename).stem
        thumb_path = os.path.join(thumbs_dir, f"thumb_{stem}.jpg")
        if os.path.exists(thumb_path):
            os.remove(thumb_path)

    if to_delete:
        logger.info("Cleaned up %d expired items.", len(to_delete))

    return to_delete


def get_storage_stats(links_db: dict, media_dir: str) -> dict:
    """Get storage statistics."""
    total_files = len(links_db)
    total_views = sum(info.get("views", 0) for info in links_db.values())
    total_size = 0

    if os.path.exists(media_dir):
        for f in os.listdir(media_dir):
            fp = os.path.join(media_dir, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)

    active_count = 0
    now = datetime.now()
    for info in links_db.values():
        try:
            expiry = datetime.fromisoformat(info["expiry"])
            max_views = info.get("max_views", 0)
            views = info.get("views", 0)
            if now <= expiry and (max_views == 0 or views < max_views):
                active_count += 1
        except (KeyError, ValueError):
            pass

    return {
        "total_links": total_files,
        "active_links": active_count,
        "total_views": total_views,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
    }
