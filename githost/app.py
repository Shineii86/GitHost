"""Flask web application for GitHost Pro."""

import hashlib
import logging
import os
import zipfile
import secrets
from datetime import datetime
from functools import wraps
from io import BytesIO

from flask import (
    Flask, request, send_file, jsonify, redirect,
    render_template_string, abort, session, make_response,
)
from flask_cors import CORS

from .templates import (
    render_home, render_gallery, render_admin,
    render_password_gate, render_error,
)
from .cleanup import cleanup_expired, get_storage_stats

logger = logging.getLogger(__name__)


def create_app(storage, config, notifier_email=None, notifier_telegram=None, shortener=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = config.server.secret_key or secrets.token_hex(32)
    CORS(app)

    ADMIN_PASSWORD = config.server.admin_password

    # --- Security helpers ---

    def require_admin(f):
        """Decorator to require admin authentication."""
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get("admin_authenticated"):
                return redirect("/admin")
            return f(*args, **kwargs)
        return decorated

    # --- Routes ---

    @app.route("/")
    def home():
        stats = get_storage_stats(storage.links_db, storage.media_dir)
        return render_home(f"/", stats)

    @app.route("/i/<link_id>", methods=["GET"])
    def serve_media(link_id):
        if link_id not in storage.links_db:
            return render_error(404, "Link not found or never existed."), 404

        info = storage.links_db[link_id]

        # Password check
        if "password_hash" in info:
            pwd = request.args.get("pwd")
            if not pwd or hashlib.sha256(pwd.encode()).hexdigest() != info["password_hash"]:
                return render_password_gate(link_id, error="Incorrect password." if pwd else ""), 403

        # Expiry check
        try:
            expiry = datetime.fromisoformat(info["expiry"])
        except (KeyError, ValueError):
            return render_error(500, "Invalid link data."), 500

        if datetime.now() > expiry:
            return render_error(410, "This link has expired."), 410

        # View limit check
        max_views = info.get("max_views", 0)
        views = info.get("views", 0)
        if max_views > 0 and views >= max_views:
            return render_error(410, "This link has reached its view limit."), 410

        # Increment views and save
        info["views"] = views + 1
        try:
            storage.save_links_db()
        except Exception as e:
            logger.warning("Failed to save view count: %s", e)

        # Notifications
        original_name = info.get("original_name", link_id)
        if notifier_email:
            notifier_email.send(
                f"GitHost: {original_name} viewed",
                f"Link {link_id} was accessed.\nViews: {info['views']}",
            )
        if notifier_telegram:
            notifier_telegram.send(f"👁️ {original_name} viewed (link {link_id}) — {info['views']} views")

        media_path = os.path.join(storage.media_dir, info["filename"])
        if not os.path.exists(media_path):
            return render_error(404, "File not found on disk."), 404

        return send_file(media_path, as_attachment=False)

    @app.route("/gallery")
    def gallery():
        active = storage.get_active_links()
        return render_gallery(active, "/")

    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        error = ""

        if request.method == "POST":
            action = request.form.get("action", "")

            # Login
            if "password" in request.form and "link_id" not in request.form:
                if request.form["password"] == ADMIN_PASSWORD:
                    session["admin_authenticated"] = True
                    return redirect("/admin")
                else:
                    error = "Incorrect password."
                    return render_admin(storage.links_db, authenticated=False, error=error)

            # Authenticated actions
            if not session.get("admin_authenticated"):
                return redirect("/admin")

            if action == "delete":
                link_id = request.form.get("link_id")
                if link_id and link_id in storage.links_db:
                    storage.remove_link(link_id)
                    logger.info("Admin deleted link: %s", link_id)

            elif action == "cleanup":
                removed = cleanup_expired(storage.links_db, storage.media_dir, storage.thumbs_dir)
                if removed:
                    storage.save_links_db()
                    logger.info("Admin triggered cleanup: %d items removed", len(removed))

            return redirect("/admin")

        if session.get("admin_authenticated"):
            return render_admin(storage.links_db, authenticated=True)

        return render_admin(storage.links_db, authenticated=False, error=error)

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin_authenticated", None)
        return redirect("/admin")

    @app.route("/download_all")
    def download_all():
        active = storage.get_active_links()
        if not active:
            return render_error(404, "No active files to download."), 404

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for link_id, info in active:
                file_path = os.path.join(storage.media_dir, info["filename"])
                if os.path.exists(file_path):
                    original_name = info.get("original_name", info["filename"])
                    zf.write(file_path, original_name)

        zip_buffer.seek(0)
        response = make_response(zip_buffer.getvalue())
        response.headers["Content-Type"] = "application/zip"
        response.headers["Content-Disposition"] = "attachment; filename=githost_export.zip"
        return response

    @app.route("/static/<path:path>")
    def serve_static(path):
        full_path = os.path.join(storage.local_dir, path)
        # Security: prevent path traversal
        real_path = os.path.realpath(full_path)
        if not real_path.startswith(os.path.realpath(storage.local_dir)):
            abort(403)
        if not os.path.exists(real_path):
            abort(404)
        return send_file(real_path)

    @app.route("/api/stats")
    def api_stats():
        """JSON stats endpoint."""
        return jsonify(get_storage_stats(storage.links_db, storage.media_dir))

    @app.route("/api/links")
    def api_links():
        """JSON list of active links (no passwords)."""
        active = storage.get_active_links()
        result = []
        for link_id, info in active:
            result.append({
                "id": link_id,
                "name": info.get("original_name", ""),
                "views": info.get("views", 0),
                "max_views": info.get("max_views", 0),
                "expiry": info.get("expiry", ""),
                "has_password": "password_hash" in info,
            })
        return jsonify(result)

    # --- Error handlers ---

    @app.errorhandler(404)
    def not_found(e):
        return render_error(404, "Page not found."), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_error(403, "Access denied."), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_error(500, "Internal server error."), 500

    return app
