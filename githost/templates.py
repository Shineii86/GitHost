"""HTML templates for GitHost web interface."""

from datetime import datetime
from typing import List, Tuple

BASE_CSS = """
:root {
    --bg: #0d1117;
    --surface: #161b22;
    --surface-2: #21262d;
    --border: #30363d;
    --text: #e6edf3;
    --text-muted: #8b949e;
    --accent: #58a6ff;
    --accent-hover: #79c0ff;
    --success: #3fb950;
    --danger: #f85149;
    --warning: #d29922;
    --radius: 8px;
    --shadow: 0 2px 8px rgba(0,0,0,0.3);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 16px 0;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(10px);
}

header .container {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

header h1 {
    font-size: 1.4em;
    font-weight: 600;
}

header h1 span { color: var(--accent); }

nav a {
    color: var(--text-muted);
    text-decoration: none;
    margin-left: 20px;
    font-size: 0.9em;
    transition: color 0.2s;
}

nav a:hover { color: var(--accent); }

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    margin: 16px 0;
    box-shadow: var(--shadow);
}

.btn {
    display: inline-block;
    padding: 8px 16px;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--text);
    cursor: pointer;
    font-size: 0.85em;
    text-decoration: none;
    transition: all 0.2s;
}

.btn:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
}

.btn-danger {
    background: transparent;
    border-color: var(--danger);
    color: var(--danger);
}

.btn-danger:hover {
    background: var(--danger);
    color: #fff;
}

.btn-success {
    background: transparent;
    border-color: var(--success);
    color: var(--success);
}

.btn-success:hover {
    background: var(--success);
    color: #fff;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
}

th, td {
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

th {
    background: var(--surface-2);
    font-weight: 600;
    font-size: 0.85em;
    text-transform: uppercase;
    color: var(--text-muted);
}

tr:hover { background: var(--surface-2); }

.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: 600;
}

.badge-active { background: rgba(63,185,80,0.15); color: var(--success); }
.badge-expired { background: rgba(248,81,73,0.15); color: var(--danger); }
.badge-limited { background: rgba(210,153,34,0.15); color: var(--warning); }

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    margin: 20px 0;
}

.gallery-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.gallery-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

.gallery-item img {
    width: 100%;
    height: 160px;
    object-fit: cover;
}

.gallery-item .info {
    padding: 10px;
}

.gallery-item .name {
    font-size: 0.85em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.gallery-item .meta {
    font-size: 0.75em;
    color: var(--text-muted);
    margin-top: 4px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin: 20px 0;
}

.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
    text-align: center;
}

.stat-card .value {
    font-size: 2em;
    font-weight: 700;
    color: var(--accent);
}

.stat-card .label {
    font-size: 0.8em;
    color: var(--text-muted);
    margin-top: 4px;
}

.search-bar {
    display: flex;
    gap: 8px;
    margin: 16px 0;
}

.search-bar input {
    flex: 1;
    padding: 8px 14px;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--text);
    font-size: 0.9em;
}

.search-bar input:focus {
    outline: none;
    border-color: var(--accent);
}

.form-group {
    margin: 12px 0;
}

.form-group label {
    display: block;
    margin-bottom: 4px;
    font-size: 0.85em;
    color: var(--text-muted);
}

.form-group input {
    width: 100%;
    padding: 8px 14px;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    background: var(--surface-2);
    color: var(--text);
    font-size: 0.9em;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
}

.empty-state .icon { font-size: 3em; margin-bottom: 16px; }

.footer {
    text-align: center;
    padding: 30px;
    color: var(--text-muted);
    font-size: 0.8em;
    border-top: 1px solid var(--border);
    margin-top: 40px;
}

.footer a { color: var(--accent); text-decoration: none; }

@media (max-width: 768px) {
    .gallery-grid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    header .container { flex-direction: column; gap: 8px; }
    nav { margin-top: 8px; }
    nav a { margin: 0 10px; }
    table { font-size: 0.85em; }
    th, td { padding: 8px; }
}
"""


def render_home(base_url: str, stats: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHost Pro</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📸 <span>GitHost</span> Pro</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/gallery">Gallery</a>
                <a href="/admin">Admin</a>
                <a href="/download_all">Download All</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <div class="card" style="text-align:center; margin-top:30px;">
            <h2 style="margin-bottom:8px;">Self-Hosted Media Sharing</h2>
            <p style="color:var(--text-muted);">Upload anything, get expiring links with password protection.</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value">{stats['active_links']}</div>
                <div class="label">Active Links</div>
            </div>
            <div class="stat-card">
                <div class="value">{stats['total_links']}</div>
                <div class="label">Total Links</div>
            </div>
            <div class="stat-card">
                <div class="value">{stats['total_views']}</div>
                <div class="label">Total Views</div>
            </div>
            <div class="stat-card">
                <div class="value">{stats['total_size_mb']} MB</div>
                <div class="label">Storage Used</div>
            </div>
        </div>
    </div>
    <div class="footer">
        <p>📸 <a href="https://github.com/Shineii86/GitHost">GitHost Pro</a> by Shinei Nouzen</p>
    </div>
</body>
</html>"""


def render_gallery(active_links: list, base_url: str) -> str:
    if not active_links:
        items_html = '<div class="empty-state"><div class="icon">📭</div><p>No active files yet. Upload some!</p></div>'
    else:
        items_html = ""
        for link_id, info in active_links:
            stem = info["filename"].rsplit(".", 1)[0]
            thumb_url = f"/static/thumbnails/thumb_{stem}.jpg"
            name = info.get("original_name", link_id)
            views = info.get("views", 0)
            max_views = info.get("max_views", 0)
            views_text = f"{views}/{max_views}" if max_views > 0 else f"{views} views"
            expiry = info.get("expiry", "")
            try:
                exp_dt = datetime.fromisoformat(expiry)
                days_left = (exp_dt - datetime.now()).days
                exp_text = f"{days_left}d left" if days_left > 0 else "Expired"
            except:
                exp_text = "—"

            items_html += f"""
            <a href="/i/{link_id}" class="gallery-item" style="text-decoration:none; color:inherit;">
                <img src="{thumb_url}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 160%22><rect fill=%22%2321262d%22 width=%22200%22 height=%22160%22/><text x=%2250%%22 y=%2250%%22 text-anchor=%22middle%22 dy=%22.3em%22 fill=%22%238b949e%22 font-size=%2240%22>📄</text></svg>'" alt="{name}">
                <div class="info">
                    <div class="name">{name}</div>
                    <div class="meta">{views_text} · {exp_text}</div>
                </div>
            </a>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gallery - GitHost Pro</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📸 <span>GitHost</span> Pro</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/gallery">Gallery</a>
                <a href="/admin">Admin</a>
                <a href="/download_all">Download All</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <h2 style="margin-top:24px;">🖼️ Gallery</h2>
        <p style="color:var(--text-muted); margin-bottom:4px;">{len(active_links)} active files</p>
        <div class="gallery-grid">
            {items_html}
        </div>
    </div>
    <div class="footer">
        <p>📸 <a href="https://github.com/Shineii86/GitHost">GitHost Pro</a> by Shinei Nouzen</p>
    </div>
</body>
</html>"""


def render_admin(links_db: dict, authenticated: bool = False, error: str = "") -> str:
    if not authenticated:
        error_html = f'<p style="color:var(--danger); margin-bottom:12px;">{error}</p>' if error else ""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - GitHost Pro</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📸 <span>GitHost</span> Pro</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/gallery">Gallery</a>
                <a href="/admin">Admin</a>
            </nav>
        </div>
    </header>
    <div class="container" style="max-width:400px; margin-top:80px;">
        <div class="card">
            <h2 style="margin-bottom:16px;">🔐 Admin Login</h2>
            {error_html}
            <form method="post">
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter admin password" autofocus>
                </div>
                <button type="submit" class="btn" style="width:100%; margin-top:8px;">Login</button>
            </form>
        </div>
    </div>
</body>
</html>"""

    # Build table rows
    rows = ""
    for link_id, info in links_db.items():
        views = info.get("views", 0)
        max_views = info.get("max_views", 0)
        views_display = f"{views}/{max_views}" if max_views > 0 else f"{views}/∞"

        try:
            expiry = datetime.fromisoformat(info["expiry"])
            now = datetime.now()
            if now > expiry:
                status = '<span class="badge badge-expired">Expired</span>'
            elif max_views > 0 and views >= max_views:
                status = '<span class="badge badge-limited">Limit Hit</span>'
            else:
                days = (expiry - now).days
                status = f'<span class="badge badge-active">{days}d left</span>'
        except:
            status = '<span class="badge badge-expired">Unknown</span>'

        created = info.get("created_at", "—")
        try:
            created = datetime.fromisoformat(created).strftime("%b %d, %H:%M")
        except:
            pass

        rows += f"""
        <tr>
            <td><code>{link_id}</code></td>
            <td>{info.get('original_name', '—')}</td>
            <td>{views_display}</td>
            <td>{status}</td>
            <td>{created}</td>
            <td>
                <form method="post" style="display:inline;">
                    <input type="hidden" name="link_id" value="{link_id}">
                    <input type="hidden" name="action" value="delete">
                    <button type="submit" class="btn btn-danger" onclick="return confirm('Delete this link?')">Delete</button>
                </form>
            </td>
        </tr>"""

    if not links_db:
        rows = '<tr><td colspan="6" style="text-align:center; color:var(--text-muted); padding:30px;">No links yet</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - GitHost Pro</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📸 <span>GitHost</span> Pro</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/gallery">Gallery</a>
                <a href="/admin">Admin</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <h2 style="margin-top:24px;">🔐 Admin Panel</h2>
        <p style="color:var(--text-muted); margin-bottom:4px;">{len(links_db)} total links</p>
        <div class="card" style="overflow-x:auto;">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>File</th>
                        <th>Views</th>
                        <th>Status</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        <form method="post" style="margin-top:16px;">
            <input type="hidden" name="action" value="cleanup">
            <button type="submit" class="btn btn-success">🧹 Cleanup Expired</button>
        </form>
    </div>
    <div class="footer">
        <p>📸 <a href="https://github.com/Shineii86/GitHost">GitHost Pro</a> by Shinei Nouzen</p>
    </div>
</body>
</html>"""


def render_password_gate(link_id: str, error: str = "") -> str:
    error_html = f'<p style="color:var(--danger); margin-bottom:12px;">{error}</p>' if error else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Protected Link - GitHost Pro</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <div class="container" style="max-width:400px; margin-top:120px;">
        <div class="card" style="text-align:center;">
            <div style="font-size:3em; margin-bottom:16px;">🔒</div>
            <h2 style="margin-bottom:8px;">Password Protected</h2>
            <p style="color:var(--text-muted); margin-bottom:16px;">This link requires a password to access.</p>
            {error_html}
            <form method="get">
                <div class="form-group">
                    <input type="password" name="pwd" placeholder="Enter password" autofocus>
                </div>
                <button type="submit" class="btn" style="width:100%; margin-top:8px;">Access File</button>
            </form>
        </div>
    </div>
</body>
</html>"""


def render_error(code: int, message: str) -> str:
    icons = {404: "🔍", 403: "🚫", 410: "💨", 500: "💥"}
    icon = icons.get(code, "❌")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{code} - GitHost Pro</title>
    <style>{BASE_CSS}</style>
</head>
<body>
    <div class="container" style="max-width:400px; margin-top:120px;">
        <div class="card" style="text-align:center;">
            <div style="font-size:4em; margin-bottom:16px;">{icon}</div>
            <h2 style="margin-bottom:8px;">{code}</h2>
            <p style="color:var(--text-muted);">{message}</p>
            <a href="/" class="btn" style="margin-top:20px;">← Go Home</a>
        </div>
    </div>
</body>
</html>"""
