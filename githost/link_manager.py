"""Advanced link management: batch operations, search, stats."""

import logging
from datetime import datetime
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


def search_links(links_db: dict, query: str) -> List[Tuple[str, dict]]:
    """Search links by filename. Returns list of (link_id, info)."""
    query = query.lower().strip()
    if not query:
        return list(links_db.items())

    results = []
    for link_id, info in links_db.items():
        name = info.get("original_name", "").lower()
        if query in name or query in link_id.lower():
            results.append((link_id, info))
    return results


def get_link_stats(info: dict) -> dict:
    """Get detailed stats for a single link."""
    views = info.get("views", 0)
    max_views = info.get("max_views", 0)
    created_at = info.get("created_at", "")
    expiry = info.get("expiry", "")

    try:
        expiry_dt = datetime.fromisoformat(expiry)
        now = datetime.now()
        days_remaining = max(0, (expiry_dt - now).days)
        hours_remaining = max(0, int((expiry_dt - now).total_seconds() / 3600))
        is_expired = now > expiry_dt
    except (ValueError, TypeError):
        days_remaining = 0
        hours_remaining = 0
        is_expired = True

    is_exhausted = max_views > 0 and views >= max_views
    is_active = not is_expired and not is_exhausted

    return {
        "views": views,
        "max_views": max_views,
        "views_remaining": max(0, max_views - views) if max_views > 0 else None,
        "days_remaining": days_remaining,
        "hours_remaining": hours_remaining,
        "is_expired": is_expired,
        "is_exhausted": is_exhausted,
        "is_active": is_active,
        "has_password": "password_hash" in info,
        "created_at": created_at,
        "expiry": expiry,
    }


def batch_delete(links_db: dict, link_ids: List[str]) -> List[str]:
    """Delete multiple links. Returns list of actually deleted IDs."""
    deleted = []
    for link_id in link_ids:
        if link_id in links_db:
            del links_db[link_id]
            deleted.append(link_id)
    return deleted


def batch_extend_expiry(links_db: dict, link_ids: List[str], extra_days: int) -> List[str]:
    """Extend expiry for multiple links. Returns list of updated IDs."""
    from datetime import timedelta
    updated = []
    for link_id in link_ids:
        if link_id in links_db:
            try:
                expiry = datetime.fromisoformat(links_db[link_id]["expiry"])
                # Only extend if not already expired
                if expiry > datetime.now():
                    new_expiry = expiry + timedelta(days=extra_days)
                    links_db[link_id]["expiry"] = new_expiry.isoformat()
                    updated.append(link_id)
                else:
                    # If expired, extend from now
                    new_expiry = datetime.now() + timedelta(days=extra_days)
                    links_db[link_id]["expiry"] = new_expiry.isoformat()
                    updated.append(link_id)
            except (ValueError, KeyError) as e:
                logger.warning("Failed to extend link %s: %s", link_id, e)
    return updated


def get_popular_links(links_db: dict, limit: int = 10) -> List[Tuple[str, dict]]:
    """Get the most viewed links."""
    sorted_links = sorted(
        links_db.items(),
        key=lambda x: x[1].get("views", 0),
        reverse=True,
    )
    return sorted_links[:limit]


def get_expiring_soon(links_db: dict, hours: int = 24) -> List[Tuple[str, dict]]:
    """Get links expiring within the specified hours."""
    from datetime import timedelta
    now = datetime.now()
    threshold = now + timedelta(hours=hours)

    expiring = []
    for link_id, info in links_db.items():
        try:
            expiry = datetime.fromisoformat(info["expiry"])
            if now < expiry <= threshold:
                expiring.append((link_id, info))
        except (ValueError, KeyError):
            pass

    return sorted(expiring, key=lambda x: x[1]["expiry"])
