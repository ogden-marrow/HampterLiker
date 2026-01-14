# 🐹 HampterLiker

> **Automatically like every video on the Hampter channel! 🎥👍**

A Python automation script that uses the YouTube Data API to like all videos from your favorite YouTube channel. Built specifically for showing love to @the_hampter! 💕

---

## ✨ Features

- 🔐 Secure OAuth 2.0 authentication
- 📺 Automatically fetches all videos from a channel
- 👍 Likes each video with progress tracking
- 🚀 Simple and easy to use
- 🐍 Python-based automation

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

### Step 3: Run the Script 🎬

```bash
python username.py
```

**What happens next:**
1. 🌐 A browser window will open for OAuth authentication
2. 🔓 Log in with your Google account and grant permissions
3. 📊 The script will fetch all videos from @the_hampter
4. 👍 Each video will be liked automatically
5. ✅ You'll see progress updates in the console

---

## 📁 Project Structure

```
HampterLiker/
├── 🐹 README.md              # You are here!
├── 📝 requirements.txt       # Python dependencies
├── 🔧 liker.py              # Core functions (auth, fetch, like)
├── 🚀 username.py           # Main script
├── 🔑 client_secret_*.json  # Your OAuth credentials
└── 📂 venv/                 # Virtual environment
```

### File Descriptions

| File | Description |
|------|-------------|
| `liker.py` | 🔧 Core functions for authentication, fetching videos, and liking |
| `username.py` | 🚀 Main script that ties everything together |
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

---

## ⚙️ Configuration

Want to like videos from a different channel? Easy! 🎯

Edit `username.py` and change line 20:

```python
channel_username = "@your_channel_name"
```

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

Feel free to fork this project and make it even better! 🌟

---

## ⚠️ Important Notes

- 📜 **Terms of Service:** Automated liking might violate YouTube's Terms of Service
- 🎓 **Educational Purpose:** Use this script responsibly and for educational purposes only
- ⏱️ **Rate Limits:** The YouTube API has quota limits - don't abuse it!
- 🔒 **Security:** Never share your `client_secret_*.json` file or commit it to public repositories

---

## 📜 License

Use this project however you want! Just be responsible! 🐹💕

---

## 💖 Show Your Support

If this helped you like all of Hampter's videos, give this repo a ⭐!

**Made with 💕 for the Hampter community**

---

### 🐹 Happy Hampting! 🐹
