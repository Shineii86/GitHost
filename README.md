<div align="center">

[![GitHost Banner](https://raw.githubusercontent.com/Shineii86/GitHost/main/images/GitHost.png)](https://github.com/Shineii86/GitHost)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shineii86/GitHost/blob/main/notebooks/GitHost.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/GitHost?style=for-the-badge)](https://github.com/Shineii86/GitHost/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/GitHost?style=for-the-badge)](https://github.com/Shineii86/GitHost/fork)

**The ultimate self-hosted media sharing platform. Upload anything, get expiring links, password protection, gallery view, admin panel, and 10+ more features — all from your phone.**

</div>

---

> 🚀 **ALL FEATURES INCLUDED**
> 
> GitHost is a complete, self-hosted alternative to services like Imgur, Dropbox shared links, or WeTransfer. It stores your files securely in your own **private GitHub repository** while providing a temporary, feature-rich public interface through a Colab-powered web server.

---

## 📖 Table of Contents

- [What is GitHost?](#-what-is-githost-pro)
- [Why Use GitHost?](#-why-use-githost-pro)
- [Complete Feature List](#-complete-feature-list)
- [Prerequisites](#-prerequisites)
- [Step-by-Step Setup Guide](#-step-by-step-setup-guide)
  - [1. Get Your GitHub Token](#1-get-your-github-token)
  - [2. Get Your ngrok Token](#2-get-your-ngrok-token)
  - [3. Optional: Email Notifications](#3-optional-email-notifications)
  - [4. Optional: Telegram Bot](#4-optional-telegram-bot)
  - [5. Optional: Bit.ly URL Shortening](#5-optional-bitly-url-shortening)
- [How to Use GitHost](#-how-to-use-githost-pro)
  - [Uploading Files](#uploading-files)
  - [Sharing Links](#sharing-links)
  - [Managing Links](#managing-links)
  - [Viewing the Gallery](#viewing-the-gallery)
- [Configuration Reference](#-configuration-reference)
- [Endpoints & URLs](#-endpoints--urls)
- [Architecture & How It Works](#-architecture--how-it-works)
- [Security Considerations](#-security-considerations)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License & Disclaimer](#-license--disclaimer)
- [Credits & Acknowledgments](#-credits--acknowledgments)

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
- **Beautiful interface** — Gallery view, QR codes, and admin panel
- **Mobile-first** — Upload directly from your phone via Google Colab

---

## ✅ Why Use GitHost?

| Feature | GitHost | Imgur | WeTransfer | Dropbox Shared Links |
|---------|-------------|-------|------------|---------------------|
| Self-hosted storage | ✅ Your GitHub | ❌ | ❌ | ❌ |
| Expiring links | ✅ Configurable | ❌ | ✅ | ✅ (Pro only) |
| View limits | ✅ Yes | ❌ | ❌ | ❌ |
| Password protection | ✅ Yes | ❌ | ✅ | ✅ |
| Gallery view | ✅ Yes | ❌ | ❌ | ❌ |
| QR codes | ✅ Yes | ❌ | ❌ | ❌ |
| Admin panel | ✅ Yes | ❌ | ❌ | ❌ |
| Free | ✅ Yes | ✅ | ✅ (5GB limit) | ✅ (limited) |
| No file size limit | ✅ GitHub's limit | 20MB | 2GB | Varies |

---

## ✨ Complete Feature List

| # | Feature | Description | How to Use |
|---|---------|-------------|------------|
| 1 | **One-Time View Links** | Links that self-destruct after being viewed once. | Set `Max views = 1` during upload. |
| 2 | **Password Protection** | Require a password to access the file. | Enter a password when prompted during upload. |
| 3 | **Multi-Format Support** | Images, videos, PDFs, ZIPs, documents. | Upload any file with supported extension. |
| 4 | **Custom Expiry Per Batch** | Set different expiry for each upload batch. | Enter custom expiry days during upload. |
| 5 | **Admin Dashboard** | View all links, view counts, and manually revoke. | Visit `/admin` with password `admin123`. |
| 6 | **QR Code Generation** | Scan to open link on another device. | Automatically displayed after upload. |
| 7 | **Automatic Thumbnails** | Image previews in gallery. | Generated for JPG, PNG, GIF files. |
| 8 | **Upload from URL** | Download from a URL instead of uploading. | Type `url` when prompted for upload method. |
| 9 | **Email Notifications** | Alerts on upload and when links are accessed. | Configure email settings in the form. |
| 10 | **Bit.ly Shortening** | Short, clean URLs for sharing. | Add your Bit.ly access token. |
| 11 | **Public Gallery** | Grid view of all active media. | Visit `/gallery`. |
| 12 | **Auto-Cleanup** | Expired files are automatically deleted. | Runs on every server start. |
| 13 | **Custom ngrok Subdomain** | Consistent URL (paid ngrok required). | Set `NGROK_SUBDOMAIN` in config. |
| 14 | **Download All as ZIP** | One-click download of all media. | Visit `/download_all`. |
| 15 | **Telegram Bot Notifications** | Get upload alerts in Telegram. | Configure bot token and chat ID. |

---

## 🛠️ Prerequisites

### Required

| Credential | Purpose | Where to Get It |
|------------|---------|-----------------|
| **GitHub Account** | Storage for your files | [github.com](https://github.com) |
| **GitHub Personal Access Token (Classic)** | API access to create/update repo | [Settings → Developer settings → Tokens (classic)](https://github.com/settings/tokens) |
| **ngrok Auth Token** | Public URL for the server | [ngrok Dashboard](https://dashboard.ngrok.com/signup) |

### Optional

| Credential | Purpose | Where to Get It |
|------------|---------|-----------------|
| **Gmail App Password** | Email notifications | [Google App Passwords](https://myaccount.google.com/apppasswords) |
| **Telegram Bot Token** | Telegram notifications | [@BotFather](https://t.me/botfather) on Telegram |
| **Bit.ly Access Token** | URL shortening | [Bit.ly API Settings](https://app.bitly.com/settings/api/) |

---

## 📋 Step-by-Step Setup Guide

### 1. Get Your GitHub Token

1. Log in to GitHub and go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
2. Click **Generate new token** → **Generate new token (classic)**.
3. Give it a name (e.g., `GitHost`).
4. Set expiration (recommended: 30 days).
5. Under **Select scopes**, check **`repo`** (this grants full control of private repositories).
6. Click **Generate token**.
7. **Copy the token immediately** (it starts with `ghp_`). You won't see it again.

> 🔒 **Security Note**: Treat this token like a password. Never commit it or share it publicly.

---

### 2. Get Your ngrok Token

1. Go to [ngrok.com](https://ngrok.com) and sign up for a free account.
2. After login, go to the [Dashboard](https://dashboard.ngrok.com).
3. Under **Getting Started** → **Your Authtoken**, copy the token.
4. Paste it into the `NGROK_AUTH_TOKEN` field in the Colab notebook.

> ℹ️ **Free Tier Limits**: ngrok free tier allows 1 online tunnel at a time, 40 connections/minute, and random subdomains. This is sufficient for personal use.

---

### 3. Optional: Email Notifications

To receive email alerts when uploads complete and when links are accessed:

1. Enable 2-Factor Authentication on your Google account.
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
3. Select **Mail** as the app and **Other** as the device (name it `GitHost`).
4. Copy the generated 16-character password.
5. In the Colab form:
   - `SEND_EMAIL = True`
   - `EMAIL_FROM` = Your Gmail address
   - `EMAIL_TO` = Recipient email (can be same)
   - `EMAIL_PASSWORD` = The 16-character app password
   - `SMTP_SERVER = smtp.gmail.com`
   - `SMTP_PORT = 465`

---

### 4. Optional: Telegram Bot

To receive upload notifications directly in Telegram:

1. Open Telegram and search for [@BotFather](https://t.me/botfather).
2. Send `/newbot` and follow the prompts to create a bot.
3. Copy the **bot token** provided.
4. Search for your bot by username and send `/start`.
5. Go to [@userinfobot](https://t.me/userinfobot) and send any message to get your **Chat ID**.
6. In the Colab form:
   - `TELEGRAM_BOT_TOKEN` = Your bot token
   - `TELEGRAM_CHAT_ID` = Your chat ID

---

### 5. Optional: Bit.ly URL Shortening

To get shorter, cleaner URLs:

1. Go to [Bit.ly](https://bitly.com) and sign up.
2. Go to [API Settings](https://app.bitly.com/settings/api/).
3. Enter your password and generate an **Access Token**.
4. Copy the token and paste into `BITLY_ACCESS_TOKEN` in Colab.

---

## 🚀 How to Use GitHost

### Uploading Files

1. **Run the notebook** in Google Colab.
2. When prompted, choose upload method:
   - `file` — Select files from your phone/computer storage
   - `url` — Paste a direct URL to an image/video/document
3. **Configure the batch**:
   ```
   Expiry in days (default 7): 3
   Max views (0=unlimited, default 0): 5
   Password (optional, press Enter to skip): mysecret
   ```
4. Wait for the upload and processing to complete.

### Sharing Links

After upload, you'll see:

```
==================================================
✅ GitHost is LIVE!
🔗 Base URL: https://abc123.ngrok.io

📸 Shareable Links:
  sunset.jpg: https://bit.ly/3xYzAbC?pwd=mysecret
  [QR Code displayed]

🖼️ Gallery: https://abc123.ngrok.io/gallery
🔐 Admin: https://abc123.ngrok.io/admin (password: admin123)
📦 Download all: https://abc123.ngrok.io/download_all
```

- **Direct Link**: Share `https://bit.ly/3xYzAbC?pwd=mysecret` with recipients.
- **QR Code**: Scan with a phone camera to open directly.

### Managing Links

Visit `/admin` in your browser:
1. Enter the admin password (default: `admin123`).
2. View a table of all active links with:
   - Link ID
   - Original filename
   - Views used / Max views
   - Expiry date
3. Click **Delete** to manually revoke any link.

### Viewing the Gallery

Visit `/gallery` to see a grid of all currently active media with thumbnails.

---

## ⚙️ Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `GITHUB_USERNAME` | string | - | Your GitHub username |
| `GITHUB_TOKEN` | string | - | GitHub PAT (classic) with `repo` scope |
| `REPO_NAME` | string | `my-image-hosting` | Repository name (auto-created if missing) |
| `NGROK_AUTH_TOKEN` | string | - | ngrok authentication token |
| `DEFAULT_EXPIRY_DAYS` | integer | `7` | Default days until link expires |
| `DEFAULT_MAX_VIEWS` | integer | `0` | Default max views (0 = unlimited) |
| `SEND_EMAIL` | boolean | `False` | Enable email notifications |
| `EMAIL_TO` | string | - | Recipient email address |
| `EMAIL_FROM` | string | - | Sender email (Gmail) |
| `EMAIL_PASSWORD` | string | - | Gmail app password |
| `SMTP_SERVER` | string | `smtp.gmail.com` | SMTP server |
| `SMTP_PORT` | integer | `465` | SMTP port |
| `TELEGRAM_BOT_TOKEN` | string | - | Telegram bot token |
| `TELEGRAM_CHAT_ID` | string | - | Telegram chat ID |
| `BITLY_ACCESS_TOKEN` | string | - | Bit.ly API access token |
| `NGROK_SUBDOMAIN` | string | - | Custom subdomain (paid ngrok) |

---

## 🌐 Endpoints & URLs

| Endpoint | Description | Access |
|----------|-------------|--------|
| `/` | Home page | Public |
| `/i/<link_id>` | Serve a specific media file | Public (with optional password) |
| `/gallery` | Grid view of all active media | Public |
| `/admin` | Admin dashboard | Password protected (`admin123`) |
| `/download_all` | Download all media as ZIP | Public |
| `/static/<path>` | Serve static files (thumbnails) | Public |

---

## 🔬 Architecture & How It Works

```
┌─────────────────┐     ┌─────────────────────┐     ┌──────────────────────┐
│  Your Phone/PC  │────▶│  Google Colab       │────▶│  Private GitHub Repo │
│  Upload Files   │     │  (Flask Server)     │     │  (Storage)           │
└─────────────────┘     └─────────────────────┘     └──────────────────────┘
                                      │
                                      │ ngrok Tunnel
                                      ▼
                        ┌─────────────────────────┐
                        │  Public Internet        │
                        │  https://xxx.ngrok.io  │
                        └─────────────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │  End Users              │
                        │  (View/Download Media)  │
                        └─────────────────────────┘
```

**Step-by-Step Flow:**

1. **Upload**: Files are uploaded from your device to the Colab environment.
2. **Storage**: Files are committed and pushed to the `media/` folder of your private GitHub repository.
3. **Database**: A `links.json` file tracks each link's metadata (expiry, views, password hash).
4. **Web Server**: A Flask server runs inside Colab, serving files from the cloned repository.
5. **Public Access**: ngrok creates a secure tunnel to `localhost:5000`, providing a public HTTPS URL.
6. **Link Management**: When a user visits `/i/<link_id>`, the server validates expiry, view count, and password before serving the file.

---

## 🔒 Security Considerations

| Aspect | Implementation |
|--------|----------------|
| **Storage** | Files are stored in YOUR private GitHub repository. Only you have access via the GitHub API. |
| **Transmission** | All traffic is encrypted via ngrok's HTTPS tunnel. |
| **Authentication** | GitHub API uses token-based authentication. Admin panel uses a simple password (change `ADMIN_PASSWORD` in code). |
| **Link Security** | Link IDs are UUIDs (unguessable). Optional password adds another layer. |
| **Expiry** | Links automatically expire after the configured duration. |
| **View Limits** | Links can be limited to a specific number of views. |
| **Data Residency** | All data remains in your GitHub account (US/EU based on GitHub's infrastructure). |

> ⚠️ **Important**: The admin password is hardcoded as `admin123` in the notebook. For production use, **change this** in the code before running.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Repository not found` | The repo will be auto-created. Ensure your token has `repo` scope. |
| `ngrok connection failed` | Check your ngrok auth token. Free tier allows only 1 simultaneous tunnel. |
| `Email not sending` | Ensure you used an **App Password**, not your regular Gmail password. Enable 2FA first. |
| `Telegram notifications not working` | Verify bot token and chat ID. Send `/start` to your bot first. |
| `Bit.ly shortening not working` | Check your access token. Bit.ly free tier allows 50 shortens/month. |
| `Gallery thumbnails not showing` | Only images (JPG, PNG, GIF) generate thumbnails. Videos won't show preview. |
| `Server stops after a few hours` | Colab runtimes disconnect after ~90 minutes of inactivity. For longer sessions, interact with the notebook periodically. |
| `Large file upload fails` | GitHub has a 100MB file size limit via API. Use Git LFS or split large files. |
| `"Link expired" but I set expiry far in future` | Check server time vs. your local time. Colab uses UTC. |

---

## ❓ FAQ

### Q: Is this really free?
**A:** Yes! GitHub (free private repos), Google Colab (free tier), ngrok (free tier), and the optional services all offer free tiers sufficient for personal use.

### Q: How long can I keep the server running?
**A:** Colab disconnects after ~90 minutes of inactivity. For longer sessions, click something in the notebook periodically. There's no way to keep it permanently online on the free tier.

### Q: Can I use a custom domain instead of ngrok?
**A:** Yes! Paid ngrok plans allow custom domains. Alternatively, you can deploy the Flask app to a free service like Render or Railway.

### Q: What happens to my files when the server stops?
**A:** Your files remain safely stored in your private GitHub repository. You can access them directly there or start a new GitHost session.

### Q: Can I upload folders?
**A:** Yes! Create a ZIP file of your folder and upload it. The ZIP will be stored as-is.

### Q: How do I change the admin password?
**A:** In the notebook code, find the line `ADMIN_PASSWORD = "admin123"` and change it to your desired password.

### Q: Can multiple people upload to the same repo?
**A:** Yes, if they have the GitHub token. Be careful sharing your token — it grants full repo access.

### Q: What file types are supported?
**A:** By default: `.jpg`, `.jpeg`, `.png`, `.gif`, `.mp4`, `.mov`, `.pdf`, `.zip`, `.txt`, `.docx`. You can edit the `ALLOWED_EXTENSIONS` set in the code.

---

## 📄 License & Disclaimer

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

> [!WARNING]
> **Disclaimer**: GitHost is intended for personal, legitimate use only. Do not use it to share copyrighted, illegal, or harmful content. The author is not responsible for any misuse of this tool. Respect GitHub's Terms of Service and rate limits.

---

## 🙏 Credits & Acknowledgments

- **Google Colab** — Free cloud Python environment
- **GitHub** — Storage and API
- **ngrok** — Secure tunneling
- **Flask** — Web framework
- **Pillow** — Image processing
- **qrcode** — QR code generation
- **python-telegram-bot** — Telegram integration

---

### 🔗 Quick Links

| Service | Link |
|---------|------|
| Google Colab | [colab.research.google.com](https://colab.research.google.com/) |
| GitHub Tokens | [github.com/settings/tokens](https://github.com/settings/tokens) |
| ngrok Dashboard | [dashboard.ngrok.com](https://dashboard.ngrok.com/) |
| Google App Passwords | [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |
| Telegram BotFather | [t.me/botfather](https://t.me/botfather) |
| Bit.ly API | [app.bitly.com/settings/api](https://app.bitly.com/settings/api/) |

---

## 💕 Loved My Work?

🚨 [Follow me on GitHub](https://github.com/Shineii86)

⭐ [Give a star to this project](https://github.com/Shineii86/GitHost)

🐛 [Report an issue](https://github.com/Shineii86/GitHost/issues)

🔧 [Contribute](https://github.com/Shineii86/GitHost/fork)

<div align="center">

<a href="https://github.com/Shineii86/GitHost">
<img src="https://github.com/Shineii86/AniPay/blob/main/Source/Banner6.png" alt="Banner">
</a>
  
  *For inquiries or collaborations*
     
[![Telegram Badge](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86 "Contact on Telegram")
[![Instagram Badge](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a "Follow on Instagram")
[![Pinterest Badge](https://img.shields.io/badge/-Pinterest-E60023?style=flat&logo=Pinterest&logoColor=white)](https://pinterest.com/ikx7a "Follow on Pinterest")
[![Gmail Badge](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com "Send an Email")

  <sup><b>Copyright © 2026 <a href="https://telegram.me/Shineii86">Shinei Nouzen</a> All Rights Reserved</b></sup>

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/GitHost?style=for-the-badge)

</div>
