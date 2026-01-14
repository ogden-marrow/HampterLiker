# 🐹 HampterLiker

> **Automatically like every video on the Hampter channel! 🎥👍**

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Functional](https://img.shields.io/badge/code%20style-functional-brightgreen.svg)](https://github.com/jpalenchar/HampterLiker)

A Python automation script that uses the YouTube Data API to like all videos from your favorite YouTube channel. Built with functional programming principles, featuring both a beautiful desktop GUI and web interface. Built specifically for showing love to @the_hampter! 💕

---

## ✨ Features

- 🖥️ **Beautiful Desktop GUI** - Standalone window with no browser needed
- 🌐 **Web Interface** - Modern web UI with real-time updates
- 🔐 **Secure OAuth 2.0** - Safe authentication with YouTube
- 📺 **Auto-fetch** - Automatically gets all videos from any channel
- 👍 **Progress Tracking** - See exactly what's happening in real-time
- 🚀 **Easy to Use** - Just enter a channel handle and click start
- 🐍 **Functional Python** - Clean, well-documented, type-hinted code
- 📊 **Live Statistics** - Watch total videos and liked count update
- 🎉 **Success Notifications** - Know when everything is complete

---

## 🚀 Quick Start

### Prerequisites

Before you begin, you'll need:
- 🐍 Python 3.6 or higher
- 📧 A Google account
- 🔑 YouTube Data API v3 credentials

---

## 🛠️ Setup Guide

### Step 1: Get Your API Credentials 🔑

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** (or select an existing one)
3. **Enable the YouTube Data API v3:**
   - Navigate to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. **Create OAuth 2.0 credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the JSON file
   - Rename it to something simple (or keep the long name)
   - Place it in the project directory

### Step 2: Install the Project 📦

```bash
# Clone the repository
git clone https://github.com/yourusername/HampterLiker.git
cd HampterLiker

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run the Application 🎬

**Option A: Desktop GUI (Recommended) 🖥️**

```bash
python gui.py
```

A beautiful standalone window will open with:
- 🐹 Cute hamster-themed interface
- 🎯 Easy channel input
- 📊 Real-time progress bar
- 📈 Live statistics
- 📜 Activity log showing what's happening
- 🎉 Success notification when complete

**No browser needed! Works completely offline after OAuth.**

**Option B: Web UI 🌐**

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

You'll see a beautiful web interface where you can:
- 🎯 Enter any YouTube channel handle
- 📊 Watch real-time progress with a progress bar
- 📈 See live stats of total videos and liked videos
- 🎉 Get a celebration when it's done!

**What happens:**
1. 🌐 A browser window will open for OAuth authentication (one-time)
2. 🔓 Log in with your Google account and grant permissions
3. 📊 The app will fetch all videos from the channel
4. 👍 Each video will be liked automatically
5. ✅ You'll see progress updates in real-time

---

## 📁 Project Structure

```
HampterLiker/
├── 🐹 README.md              # You are here!
├── 📝 requirements.txt       # Python dependencies
├── 🖥️  gui.py                # Standalone desktop GUI (NEW! ⭐)
├── 🌐 app.py                # Flask web UI
├── ⚙️  config.py             # Configuration management
├── 🔧 youtube_service.py    # Core YouTube service (functional)
├── 📂 templates/            # HTML templates
│   └── index.html           # Beautiful web interface
├── 🔑 client_secret_*.json  # Your OAuth credentials
└── 📂 venv/                 # Virtual environment
```

### File Descriptions

| File | Description |
|------|-------------|
| `gui.py` | 🖥️ **Standalone desktop GUI** with tkinter (no browser needed!) |
| `app.py` | 🌐 Flask web server with beautiful UI |
| `config.py` | ⚙️ Immutable configuration with dataclasses |
| `youtube_service.py` | 🔧 Core YouTube API service (pure functional programming) |
| `templates/index.html` | 🎨 Web interface with progress tracking |
| `requirements.txt` | 📦 Python package dependencies |
| `client_secret_*.json` | 🔑 Your OAuth 2.0 credentials from Google |

---

## 🐛 Troubleshooting

### ❌ Error 401: deleted_client

**Problem:**
```
Access blocked: Authorization Error
Error 401: deleted_client
The OAuth client was deleted.
```

**Solution:**

This error occurs when the OAuth client ID has been deleted from your Google Cloud Console. Here's how to fix it:

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)** 🌐
2. **Navigate to your project**
3. **Go to "APIs & Services" > "Credentials"** 🔑
4. **Check if your OAuth 2.0 Client ID exists:**
   - ❌ If it's missing/deleted → You need to create a new one
   - ✅ If it exists → Download a fresh copy of the JSON file

5. **Create a NEW OAuth 2.0 Client ID:**
   - Click "**+ CREATE CREDENTIALS**"
   - Select "**OAuth client ID**"
   - Choose "**Desktop app**" as application type
   - Give it a name (e.g., "HampterLiker Desktop")
   - Click "**Create**"
   - Download the JSON file

6. **Replace the old credentials file:**
   - Delete the old `client_secret_*.json` file from your project
   - Move the newly downloaded JSON file to your project directory
   - Update the filename in `liker.py` line 8:
     ```python
     client_secrets_file = "your_new_client_secret_file.json"
     ```

7. **Delete any cached tokens:**
   ```bash
   rm token.json token.pickle
   ```

8. **Run the script again:**
   ```bash
   python username.py
   ```

### 🔒 Other Common Issues

#### "The authentication flow has expired"
- **Solution:** Close the browser tab and run the script again

#### "Access Not Configured"
- **Solution:** Make sure YouTube Data API v3 is enabled in your Google Cloud project

#### "Invalid grant: account not found"
- **Solution:** Make sure you're logging in with the correct Google account

#### "macOS 15 (1507) or later required" / tkinter crash
- **Problem:** Desktop GUI may not work with certain Python/macOS combinations
- **Solution 1 (Recommended):** Use the web interface:
  ```bash
  python app.py
  # Then open http://localhost:5000
  ```
- **Solution 2:** Upgrade Python using pyenv:
  ```bash
  pyenv install 3.11.0
  pyenv local 3.11.0
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

---

## ⚙️ Configuration

Want to like videos from a different channel? Easy! 🎯

Just enter any channel handle in the GUI or web interface:
- `@pewdiepie`
- `@mrbeast`
- `@any_channel_you_want`

The app will automatically find and like all videos from that channel!

---

## 📊 What the Script Does

```
┌─────────────────────────────────────┐
│  1. 🔐 Authenticate with YouTube    │
│  2. 🔍 Find channel by username     │
│  3. 📺 Fetch all videos (50 at a    │
│     time, handles pagination)       │
│  4. 👍 Like each video one by one   │
│  5. ✅ Show progress & completion   │
└─────────────────────────────────────┘
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas we'd love help with:
- 🧪 Unit tests
- 🎨 UI improvements
- 📝 Documentation
- 🐛 Bug fixes
- ✨ New features

Feel free to fork this project and make it even better! 🌟

---

## ⚠️ Important Notes

- 📜 **Terms of Service:** Automated liking might violate YouTube's Terms of Service
- 🎓 **Educational Purpose:** Use this script responsibly and for educational purposes only
- ⏱️ **Rate Limits:** The YouTube API has quota limits - don't abuse it!
- 🔒 **Security:** Never share your `client_secret_*.json` file or commit it to public repositories

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Use this project however you want! Just be responsible! 🐹💕

---

## 💖 Show Your Support

If this helped you like all of Hampter's videos, give this repo a ⭐!

**Made with 💕 for the Hampter community**

---

### 🐹 Happy Hampting! 🐹
