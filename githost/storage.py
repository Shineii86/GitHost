"""GitHub-based storage backend for GitHost."""

import os
import time
import json
import shutil
import logging
from pathlib import Path
from typing import Optional

import requests
from github import Github, GithubException

logger = logging.getLogger(__name__)


class GitHubStorage:
    """Manages file storage in a private GitHub repository."""

    def __init__(self, username: str, token: str, repo_name: str, local_dir: str = "/content/repo"):
        self.username = username
        self.token = token
        self.repo_name = repo_name
        self.local_dir = local_dir
        self.media_dir = os.path.join(local_dir, "media")
        self.thumbs_dir = os.path.join(local_dir, "thumbnails")
        self.links_db_path = os.path.join(local_dir, "links.json")

        self._github = Github(token)
        self._repo = None
        self._links_db: dict = {}

    @property
    def repo(self):
        if self._repo is None:
            raise RuntimeError("Repository not initialized. Call setup() first.")
        return self._repo

    @property
    def links_db(self) -> dict:
        return self._links_db

    def setup(self) -> None:
        """Ensure repo exists, clone it, and load the links database."""
        self._ensure_repo_exists()
        self._clone_repo()
        self._load_links_db()
        os.makedirs(self.media_dir, exist_ok=True)
        os.makedirs(self.thumbs_dir, exist_ok=True)

    def _ensure_repo_exists(self) -> None:
        """Create the private repo if it doesn't exist."""
        url = f"https://api.github.com/repos/{self.username}/{self.repo_name}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            logger.info("Repository '%s' exists.", self.repo_name)
            return
        if resp.status_code == 404:
            logger.info("Creating private repo '%s'...", self.repo_name)
            create_data = {"name": self.repo_name, "private": True, "auto_init": True}
            create_resp = requests.post(
                "https://api.github.com/user/repos",
                headers=headers,
                json=create_data,
            )
            if create_resp.status_code == 201:
                logger.info("Repository created successfully.")
                time.sleep(3)
                return
            raise RuntimeError(f"Failed to create repo: {create_resp.text}")
        raise RuntimeError(f"GitHub API error: {resp.text}")

    def _clone_repo(self) -> None:
        """Clone the repository locally."""
        from git import Repo as GitRepo

        if os.path.exists(self.local_dir):
            shutil.rmtree(self.local_dir)
        repo_url = f"https://{self.username}:{self.token}@github.com/{self.username}/{self.repo_name}.git"
        self._repo = GitRepo.clone_from(repo_url, self.local_dir)
        logger.info("Repository cloned to %s", self.local_dir)

    def _load_links_db(self) -> None:
        """Load the links database from the repo."""
        if os.path.exists(self.links_db_path):
            with open(self.links_db_path, "r") as f:
                self._links_db = json.load(f)
        else:
            self._links_db = {}

    def save_links_db(self) -> None:
        """Save links DB and push to GitHub."""
        with open(self.links_db_path, "w") as f:
            json.dump(self._links_db, f, indent=2)
        self.repo.index.add(["links.json"])
        self.repo.index.commit("Update links database")
        self.repo.remote(name="origin").push()

    def add_link(self, link_id: str, link_info: dict) -> None:
        """Add a link entry and persist."""
        self._links_db[link_id] = link_info
        self.save_links_db()

    def remove_link(self, link_id: str) -> Optional[str]:
        """Remove a link and its files. Returns the filename if deleted."""
        if link_id not in self._links_db:
            return None
        info = self._links_db.pop(link_id)
        filename = info.get("filename", "")

        # Remove media file
        media_path = os.path.join(self.media_dir, filename)
        if os.path.exists(media_path):
            os.remove(media_path)

        # Remove thumbnail
        stem = Path(filename).stem
        thumb_path = os.path.join(self.thumbs_dir, f"thumb_{stem}.jpg")
        if os.path.exists(thumb_path):
            os.remove(thumb_path)

        self.save_links_db()
        return filename

    def commit_media(self) -> None:
        """Commit and push media files."""
        self.repo.index.add(["media/*", "thumbnails/*"])
        self.repo.index.commit("Add media")
        self.repo.remote(name="origin").push()

    def get_active_links(self) -> list:
        """Return list of (link_id, info) for non-expired, non-exhausted links."""
        from datetime import datetime
        now = datetime.now()
        active = []
        for link_id, info in self._links_db.items():
            expiry = datetime.fromisoformat(info["expiry"])
            max_views = info.get("max_views", 0)
            views = info.get("views", 0)
            if now <= expiry and (max_views == 0 or views < max_views):
                active.append((link_id, info))
        return active
