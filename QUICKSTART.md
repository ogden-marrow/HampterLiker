# ⚡ Quick Start Guide

Get HampterLiker running in 5 minutes! 🐹

## 1. 📋 Prerequisites Check

Make sure you have:
- ✅ Python 3.6 or higher
- ✅ A Google account
- ✅ 5 minutes of time

Check your Python version:
```bash
python --version
# or
python3 --version
```

## 2. 🔑 Get YouTube API Credentials

### Step-by-Step:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Click "**Select a Project**" → "**New Project**"
   - Name it: `HampterLiker`
   - Click "**Create**"

3. Enable YouTube Data API:
   - Click "**≡**" menu → "**APIs & Services**" → "**Library**"
   - Search: `YouTube Data API v3`
   - Click it → Click "**Enable**"

4. Create OAuth Credentials:
   - Go to "**APIs & Services**" → "**Credentials**"
   - Click "**+ CREATE CREDENTIALS**"
   - Select "**OAuth client ID**"

   - If prompted for OAuth consent screen:
     - Choose "**External**"
     - App name: `HampterLiker`
     - Your email for support
     - Click "**Save and Continue**" through the steps
     - Add yourself as a test user

   - Back in Credentials:
     - Application type: "**Desktop app**"
     - Name: `HampterLiker Desktop`
     - Click "**Create**"

5. Download the JSON file:
   - Click "**⬇ Download JSON**"
   - Save it to your Downloads folder

## 3. 📦 Install HampterLiker

```bash
# Clone the repository
git clone https://github.com/jpalenchar/HampterLiker.git
cd HampterLiker

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## 4. 🔐 Add Your Credentials

Move the downloaded JSON file to the HampterLiker directory:

```bash
# From your Downloads folder
mv ~/Downloads/client_secret_*.json .
```

Or just drag and drop it into the `HampterLiker` folder!

## 5. 🚀 Run It!

### Desktop GUI (Recommended):
```bash
python gui.py
```

A beautiful window will open! 🖥️

### Web Interface:
```bash
python app.py
```

Then open: http://localhost:5000 🌐

## 6. 🎉 Use It!

1. **Authentication** (First time only):
   - A browser will open
   - Log in with your Google account
   - Click "Allow"
   - Close the browser

2. **Like Videos**:
   - Enter a channel handle (e.g., `@the_hampter`)
   - Click "Start Liking Videos!"
   - Watch the progress! 📊

## 🆘 Troubleshooting

### "No module named 'google'"
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

### "No client_secret_*.json file found"
```bash
# Make sure the credentials file is in the project directory
ls client_secret_*.json

# If not found, download it again from Google Cloud Console
```

### "Error 401: deleted_client"
Your OAuth credentials were deleted. Create new ones:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Follow Step 2 again
3. Delete old credentials: `rm client_secret_*.json`
4. Add new credentials file

### "Access Not Configured"
YouTube Data API isn't enabled:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. APIs & Services → Library
3. Search "YouTube Data API v3"
4. Click "Enable"

### "macOS 15 (1507) or later required" or tkinter issues
The GUI has issues with your Python/tkinter version. Use the web interface instead:
```bash
python app.py
# Then open http://localhost:5000
```

Or upgrade Python:
```bash
# Using pyenv
pyenv install 3.11.0
pyenv local 3.11.0
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Quota Exceeded" Error
YouTube API has daily quota limits (10,000 units per day for free tier):
- **What happened**: You've reached the daily API quota limit
- **Solution**: Wait until midnight Pacific Time when quotas reset
- **How much quota**: Each video like uses ~50 units, so ~200 videos/day max
- **Don't worry**: The app saves your progress and will continue from where it stopped
- **Try again tomorrow**: Just run the app again after the quota resets!

## 💡 Tips

- **First run takes longer** - OAuth setup happens
- **Subsequent runs are faster** - Credentials cached
- **API Quota Limits** - YouTube API has daily quota limits (10,000 units/day for free tier)
- **Quota Exceeded?** - The app will stop gracefully and tell you. Try again tomorrow!
- **Quota Resets Daily** - Midnight Pacific Time
- **Be patient** - Large channels take time
- **Check logs** - Watch the activity log for issues

## 🎯 Next Steps

- ⭐ Star the repository on GitHub
- 🐛 Report bugs in [Issues](https://github.com/jpalenchar/HampterLiker/issues)
- 🤝 Contribute (see [CONTRIBUTING.md](CONTRIBUTING.md))
- 📖 Learn about the code ([CODE_STRUCTURE.md](CODE_STRUCTURE.md))

## 📱 Need Help?

1. Check [README.md](README.md) for full documentation
2. Open an issue on GitHub
3. Make sure you followed all steps above

---

**You're ready to like all of Hampter's videos! 🐹✨**
