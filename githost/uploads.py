"""File upload and processing logic."""

import os
import uuid
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests
from PIL import Image

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg",
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".pdf", ".zip", ".rar", ".7z",
    ".txt", ".md", ".docx", ".xlsx", ".pptx",
    ".mp3", ".wav", ".ogg", ".flac",
}

# Max file size: 100MB (GitHub API limit)
MAX_FILE_SIZE = 100 * 1024 * 1024


class UploadResult:
    """Result of a file upload operation."""

    def __init__(self, original_name: str, safe_filename: str, link_id: str,
                 file_path: str, thumb_path: Optional[str] = None):
        self.original_name = original_name
        self.safe_filename = safe_filename
        self.link_id = link_id
        self.file_path = file_path
        self.thumb_path = thumb_path


def detect_extension_from_url(url: str, content_type: str) -> str:
    """Detect file extension from URL or content-type."""
    # Try URL path first
    path = Path(url.split("?")[0])
    if path.suffix and path.suffix.lower() in ALLOWED_EXTENSIONS:
        return path.suffix.lower()

    # Fall back to content-type
    type_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "video/mp4": ".mp4",
        "video/quicktime": ".mov",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/plain": ".txt",
    }
    for ct, ext in type_map.items():
        if ct in content_type:
            return ext
    return ".bin"


def generate_thumbnail(file_path: str, thumb_dir: str, file_id: str, max_size: tuple = (300, 300)) -> Optional[str]:
    """Generate a thumbnail for image files. Returns thumb path or None."""
    try:
        img = Image.open(file_path)
        img.thumbnail(max_size)

        # Convert RGBA to RGB for JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        thumb_path = os.path.join(thumb_dir, f"thumb_{file_id}.jpg")
        img.save(thumb_path, "JPEG", quality=85)
        return thumb_path
    except Exception as e:
        logger.warning("Thumbnail generation failed for %s: %s", file_path, e)
        return None


def process_upload_from_file(data: bytes, filename: str, media_dir: str,
                              thumb_dir: str) -> Optional[UploadResult]:
    """Process an uploaded file: validate, save, generate thumbnail."""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.warning("Skipping %s — unsupported format (%s)", filename, ext)
        return None

    if len(data) > MAX_FILE_SIZE:
        logger.warning("Skipping %s — file too large (%d bytes)", filename, len(data))
        return None

    file_id = uuid.uuid4().hex[:8]
    safe_filename = f"{file_id}{ext}"
    file_path = os.path.join(media_dir, safe_filename)

    with open(file_path, "wb") as f:
        f.write(data)

    thumb_path = None
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}:
        thumb_path = generate_thumbnail(file_path, thumb_dir, file_id)

    return UploadResult(
        original_name=filename,
        safe_filename=safe_filename,
        link_id=str(uuid.uuid4())[:8],
        file_path=file_path,
        thumb_path=thumb_path,
    )


def process_upload_from_url(url: str, media_dir: str, thumb_dir: str,
                             timeout: int = 30) -> Optional[UploadResult]:
    """Download a file from URL and process it."""
    try:
        resp = requests.get(url, timeout=timeout, stream=True, allow_redirects=True)
        resp.raise_for_status()

        content_type = resp.headers.get("content-type", "")
        ext = detect_extension_from_url(url, content_type)
        file_id = uuid.uuid4().hex[:8]
        safe_filename = f"{file_id}{ext}"
        file_path = os.path.join(media_dir, safe_filename)

        # Stream to disk to handle large files
        total_size = 0
        with open(file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    f.close()
                    os.remove(file_path)
                    logger.warning("URL download too large, aborting.")
                    return None
                f.write(chunk)

        # Get original filename from URL or content-disposition
        original_name = url.split("/")[-1].split("?")[0] or "download"
        if "." not in original_name:
            original_name += ext

        thumb_path = None
        if ext in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}:
            thumb_path = generate_thumbnail(file_path, thumb_dir, file_id)

        return UploadResult(
            original_name=original_name,
            safe_filename=safe_filename,
            link_id=str(uuid.uuid4())[:8],
            file_path=file_path,
            thumb_path=thumb_path,
        )
    except Exception as e:
        logger.error("URL download failed: %s", e)
        return None


def create_link_entry(result: UploadResult, expiry_days: int, max_views: int,
                       password: Optional[str] = None) -> dict:
    """Create a link database entry."""
    entry = {
        "filename": result.safe_filename,
        "expiry": (datetime.now() + timedelta(days=expiry_days)).isoformat(),
        "views": 0,
        "max_views": max_views,
        "original_name": result.original_name,
        "created_at": datetime.now().isoformat(),
    }
    if password:
        entry["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
    return entry
