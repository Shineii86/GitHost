<div align="center">

[![GitHost Banner](https://raw.githubusercontent.com/Shineii86/GitHost/main/images/GitHost.png)](https://github.com/Shineii86/GitHost)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shineii86/GitHost/blob/main/notebooks/GitHost.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/GitHost?style=for-the-badge)](https://github.com/Shineii86/GitHost/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/GitHost?style=for-the-badge)](https://github.com/Shineii86/GitHost/fork)

**The ultimate self-hosted media sharing platform. Upload anything, get expiring links, password protection, gallery view, admin panel, and 15+ more features — all from your phone.**

</div>

---

> 🚀 **v2.0 — NOW MODULAR & IMPROVED**
> 
> GitHost is a complete, self-hosted alternative to services like Imgur, Dropbox shared links, or WeTransfer. It stores your files securely in your own **private GitHub repository** while providing a temporary, feature-rich public interface through a Colab-powered web server.

---

## 📖 Table of Contents

- [What is GitHost?](#-what-is-githost)
- [Why Use GitHost?](#-why-use-githost)
- [✨ What's New in v2.0](#-whats-new-in-v20)
- [Complete Feature List](#-complete-feature-list)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Step-by-Step Setup Guide](#-step-by-step-setup-guide)
- [How to Use GitHost](#-how-to-use-githost)
- [Configuration Reference](#-configuration-reference)
- [Endpoints & URLs](#-endpoints--urls)
- [API Reference](#-api-reference)
- [Architecture](#-architecture)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License](#-license)
- [Credits](#-credits)

---

## 🎯 What is GitHost?

**GitHost** solves a universal problem: you want to share a file (photo, video, document) with someone, but you don't want to:

- Upload it to a public service where you lose control
- Have the link live forever
- Worry about who might access it

With GitHost, you get:

- **Full control** — Files are stored in YOUR private GitHub repository
- **Temporary access** — Links expire after a set number of days
- **View limits** — Links can self-destruct after N views
- **Password protection** — Optional password required to access
- **Beautiful interface** — Dark-themed gallery, QR codes, and admin panel
- **Mobile-first** — Upload directly from your phone via Google Colab

---

## ✅ Why Use GitHost?

| Feature | GitHost | Imgur | WeTransfer | Dropbox |
|---------|---------|-------|------------|---------|
| Self-hosted storage | ✅ Your GitHub | ❌ | ❌ | ❌ |
| Expiring links | ✅ Configurable | ❌ | ✅ | ✅ (Pro) |
| View limits | ✅ Yes | ❌ | ❌ | ❌ |
| Password protection | ✅ Yes | ❌ | ✅ | ✅ |
| Gallery view | ✅ Yes | ❌ | ❌ | ❌ |
| QR codes | ✅ Yes | ❌ | ❌ | ❌ |
| Admin panel | ✅ Yes | ❌ | ❌ | ❌ |
| JSON API | ✅ Yes | ❌ | ❌ | ❌ |
| Free | ✅ Yes | ✅ | ✅ (5GB) | ✅ (limited) |

---

## 🆕 What's New in v2.0

| Improvement | Description |
|-------------|-------------|
| 🏗️ **Modular Architecture** | Refactored from monolithic notebook into clean Python package |
| 🎨 **Dark-Themed UI** | Beautiful responsive interface with proper design system |
| 🔐 **Session-Based Admin** | No more password on every request — login once |
| 🛡️ **CSRF Protection** | Tokens on all admin forms |
| ⏱️ **Rate Limiting** | 60 req/min on media, 10 req/min on admin |
| 🔒 **Security Headers** | CSP, X-Frame-Options, X-Content-Type-Options |
| 🚫 **SSRF Prevention** | URL validation blocks private/internal IPs |
| 📊 **Stats Dashboard** | Home page shows active links, views, storage |
| 🔍 **Search API** | Search links by filename |
| 📄 **Link Detail Pages** | `/info/<id>` with full stats |
| 🌐 **JSON API** | `/api/stats`, `/api/search`, `/api/popular`, `/api/expiring` |
| 📁 **More File Types** | Audio, webp, svg, docx, xlsx, pptx support |
| 🧹 **Manual Cleanup** | Button in admin to purge expired links |
| 📦 **Better ZIP Export** | Original filenames preserved in downloads |
| 🖼️ **Better Thumbnails** | RGBA→RGB conversion, JPEG quality tuning |

---

## ✨ Complete Feature List

| # | Feature | Description |
|---|---------|-------------|
| 1 | One-Time View Links | Self-destruct after 1 view |
| 2 | Password Protection | Optional password per batch |
| 3 | Multi-Format Support | Images, videos, PDFs, ZIPs, audio, docs |
| 4 | Custom Expiry Per Batch | Different expiry for each upload |
| 5 | Admin Dashboard | `/admin` with session auth & delete |
| 6 | QR Code Generation | For every shareable link |
| 7 | Automatic Thumbnails | Image previews in gallery |
| 8 | Upload from URL | Paste URL instead of file upload |
| 9 | Email Notifications | On upload and link access |
| 10 | Bit.ly URL Shortening | Clean, short URLs |
| 11 | Public Gallery | `/gallery` with dark theme |
| 12 | Auto-Cleanup | Expired files auto-deleted |
| 13 | Custom ngrok Subdomain | Consistent URL (paid) |
| 14 | Download All as ZIP | `/download_all` with original names |
| 15 | Telegram Bot | Upload/access alerts |
| 16 | JSON API | Stats, search, popular, expiring |
| 17 | Link Detail Pages | `/info/<id>` with full stats |
| 18 | Storage Dashboard | Stats on home page |

---

## 📁 Project Structure

```
GitHost/
├── notebooks/
│   └── GitHost.ipynb          # Colab notebook (main entry point)
├── githost/
│   ├── __init__.py             # Package metadata
│   ├── __main__.py             # CLI entry point
│   ├── app.py                  # Flask application & routes
│   ├── cleanup.py              # Expired link cleanup
│   ├── config.py               # Configuration management
│   ├── link_manager.py         # Search, stats, batch operations
│   ├── notifications.py        # Email & Telegram notifiers
│   ├── security.py             # CSRF, rate limiting, validation
│   ├── shortener.py            # Bit.ly URL shortening
│   ├── storage.py              # GitHub storage backend
│   ├── templates.py            # HTML templates (dark theme)
│   └── uploads.py              # File upload & processing
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## 🛠️ Prerequisites

### Required

| Credential | Purpose | Where to Get It |
|------------|---------|-----------------|
| GitHub Account | Storage | [github.com](https://github.com) |
| GitHub PAT (Classic) | API access | [Settings → Tokens](https://github.com/settings/tokens) |
| ngrok Auth Token | Public URL | [ngrok Dashboard](https://dashboard.ngrok.com/signup) |

### Optional

| Credential | Purpose | Where to Get It |
|------------|---------|-----------------|
| Gmail App Password | Email alerts | [Google App Passwords](https://myaccount.google.com/apppasswords) |
| Telegram Bot Token | Telegram alerts | [@BotFather](https://t.me/botfather) |
| Bit.ly Access Token | URL shortening | [Bit.ly API](https://app.bitly.com/settings/api/) |

---

## 📋 Step-by-Step Setup Guide

### 1. Get Your GitHub Token

1. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token** → **Generate new token (classic)**
3. Name it `GitHost`, set expiration (30 days recommended)
4. Check **`repo`** scope
5. Click **Generate token** and **copy it immediately** (starts with `ghp_`)

> 🔒 Treat this token like a password. Never commit it or share it publicly.

### 2. Get Your ngrok Token

1. Sign up at [ngrok.com](https://ngrok.com)
2. Go to [Dashboard](https://dashboard.ngrok.com) → copy your **Authtoken**
3. Paste into `NGROK_AUTH_TOKEN` in Colab

> ℹ️ Free tier: 1 tunnel, 40 connections/min, random subdomains.

### 3–5. Optional Integrations

<details>
<summary>📧 Email Notifications</summary>

1. Enable 2FA on Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords) for Mail
3. Set `SEND_EMAIL = True` and fill in email fields
</details>

<details>
<summary>🤖 Telegram Bot</summary>

1. Create bot via [@BotFather](https://t.me/botfather)
2. Get your Chat ID from [@userinfobot](https://t.me/userinfobot)
3. Fill in `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
</details>

<details>
<summary>🔗 Bit.ly Shortening</summary>

1. Sign up at [bitly.com](https://bitly.com)
2. Generate Access Token in [API Settings](https://app.bitly.com/settings/api/)
3. Fill in `BITLY_ACCESS_TOKEN`
</details>

---

## 🚀 How to Use GitHost

### Uploading Files

1. Run the notebook in Google Colab
2. Choose upload method: `file` (device storage) or `url` (direct link)
3. Configure the batch:
   ```
   Expiry in days (default 7): 3
   Max views (0=unlimited, default 0): 5
   Password (optional): mysecret
   ```

### After Upload

```
==================================================
✅ GitHost Pro v2.0 is LIVE!
🔗 Base URL: https://abc123.ngrok.io

📸 Shareable Links:
  sunset.jpg: https://bit.ly/3xYzAbC?pwd=mysecret

🖼️ Gallery:  https://abc123.ngrok.io/gallery
🔐 Admin:    https://abc123.ngrok.io/admin
📦 Download: https://abc123.ngrok.io/download_all
📊 Stats:    https://abc123.ngrok.io/api/stats
```

### Admin Panel

Visit `/admin` → enter password → view all links with:
- Link ID, filename, views, status, created date
- Delete buttons with confirmation
- Manual cleanup of expired links

---

## ⚙️ Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `GITHUB_USERNAME` | string | — | Your GitHub username |
| `GITHUB_TOKEN` | string | — | GitHub PAT with `repo` scope |
| `REPO_NAME` | string | `my-image-hosting` | Repository name |
| `NGROK_AUTH_TOKEN` | string | — | ngrok auth token |
| `DEFAULT_EXPIRY_DAYS` | int | `7` | Default link expiry |
| `DEFAULT_MAX_VIEWS` | int | `0` | Default max views (0=∞) |
| `ADMIN_PASSWORD` | string | `admin123` | Admin panel password |
| `SEND_EMAIL` | bool | `false` | Enable email notifications |
| `EMAIL_TO` / `EMAIL_FROM` | string | — | Email addresses |
| `EMAIL_PASSWORD` | string | — | Gmail app password |
| `TELEGRAM_BOT_TOKEN` | string | — | Telegram bot token |
| `TELEGRAM_CHAT_ID` | string | — | Telegram chat ID |
| `BITLY_ACCESS_TOKEN` | string | — | Bit.ly API token |
| `NGROK_SUBDOMAIN` | string | — | Custom subdomain (paid) |

---

## 🌐 Endpoints & URLs

| Endpoint | Description | Access |
|----------|-------------|--------|
| `/` | Home page with stats | Public |
| `/i/<link_id>` | Serve media file | Public (optional password) |
| `/info/<link_id>` | Link detail page | Public |
| `/gallery` | Grid view of active media | Public |
| `/admin` | Admin dashboard | Password protected |
| `/download_all` | Download all as ZIP | Public |
| `/static/<path>` | Static files (thumbnails) | Public |

---

## 📡 API Reference

All API endpoints return JSON.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats` | GET | Storage stats (links, views, size) |
| `/api/links` | GET | List all active links |
| `/api/search?q=<query>` | GET | Search links by filename |
| `/api/link/<link_id>` | GET | Detailed link stats |
| `/api/popular?limit=10` | GET | Most viewed links |
| `/api/expiring?hours=24` | GET | Links expiring soon |

### Example: `/api/stats`
```json
{
  "total_links": 15,
  "active_links": 12,
  "total_views": 847,
  "total_size_bytes": 52428800,
  "total_size_mb": 50.0
}
```

---

## 🔬 Architecture

```
┌─────────────────┐     ┌─────────────────────┐     ┌──────────────────────┐
│  Your Phone/PC  │────▶│  Google Colab       │────▶│  Private GitHub Repo │
│  Upload Files   │     │  (Flask + githost/)  │     │  (Storage)           │
└─────────────────┘     └─────────────────────┘     └──────────────────────┘
                                      │
                                      │ ngrok Tunnel
                                      ▼
                        ┌─────────────────────────┐
                        │  Public Internet        │
                        │  https://xxx.ngrok.io   │
                        └─────────────────────────┘
```

**Flow:** Upload → Colab → GitHub Repo → Flask Server → ngrok → Public URL

---

## 🔒 Security

| Layer | Implementation |
|-------|----------------|
| Storage | Private GitHub repo, token-authenticated API |
| Transport | HTTPS via ngrok tunnel |
| Links | UUID-based IDs (unguessable) |
| Passwords | SHA-256 hashed, never stored in plain text |
| Admin | Session-based auth with CSRF tokens |
| Rate Limiting | 60 req/min (media), 10 req/min (admin) |
| Headers | CSP, X-Frame-Options, X-Content-Type-Options |
| SSRF Protection | URL validation blocks private/internal IPs |
| Path Traversal | Real-path checks on static file serving |

> ⚠️ Change `ADMIN_PASSWORD` from `admin123` before production use.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Repository not found | Auto-created. Ensure token has `repo` scope. |
| ngrok failed | Check auth token. Free tier = 1 simultaneous tunnel. |
| Email not sending | Use App Password, not regular password. Enable 2FA. |
| Telegram not working | Verify token & chat ID. Send `/start` to bot first. |
| Bit.ly not working | Check token. Free tier = 50 shortens/month. |
| Thumbnails missing | Only JPG/PNG/GIF generate thumbnails. |
| Server stops | Colab disconnects after ~90 min inactivity. |
| Upload fails | GitHub API limit: 100MB per file. |
| Timezone mismatch | Colab uses UTC. Check server time. |

---

## ❓ FAQ

**Is it really free?** Yes — GitHub free repos, Colab free tier, ngrok free tier.

**How long can it run?** Colab disconnects after ~90 min of inactivity. Interact periodically.

**Custom domain?** Yes — paid ngrok plans, or deploy Flask to Render/Railway.

**What happens when server stops?** Files stay in your GitHub repo. Start a new session anytime.

**Can I upload folders?** Yes — ZIP them first.

**Multiple uploaders?** Yes, if they have the GitHub token.

**Supported file types?** `.jpg` `.jpeg` `.png` `.gif` `.webp` `.bmp` `.svg` `.mp4` `.mov` `.avi` `.mkv` `.webm` `.mp3` `.wav` `.ogg` `.flac` `.pdf` `.zip` `.rar` `.7z` `.txt` `.md` `.docx` `.xlsx` `.pptx`

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file.

> [!WARNING]
> GitHost is for personal, legitimate use only. Don't share copyrighted, illegal, or harmful content. Respect GitHub's ToS.

---

## 🙏 Credits

[Google Colab](https://colab.research.google.com/) · [GitHub](https://github.com) · [ngrok](https://ngrok.com) · [Flask](https://flask.palletsprojects.com/) · [Pillow](https://python-pillow.org/) · [qrcode](https://pypi.org/project/qrcode/) · [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)

---

<div align="center">

**Copyright [Shinei Nouzen](https://github.com/Shineii86) All Rights Reserved.**

*Made with ❤️ for ultimate self-hosted sharing*

[![Telegram](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86)
[![Instagram](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a)
[![Gmail](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com)

⭐ [Star this repo](https://github.com/Shineii86/GitHost) · 🐛 [Report issue](https://github.com/Shineii86/GitHost/issues) · 🔧 [Contribute](https://github.com/Shineii86/GitHost/fork)

</div>
