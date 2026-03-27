# Discord Music Bot 🎵

A feature-rich Discord music bot built with Python, designed to bring seamless music streaming to your Discord server. This bot integrates YouTube music search, AI-powered chatbot functionality, and an intuitive interactive control interface.

## 🚀 Features

### Core Music Functionality
- **YouTube Search & Streaming**: Search and play music directly from YouTube using `yt-dlp`
- **Music Queue System**: Queue multiple songs with automatic queue management
- **Playback Controls**: 
  - ▶️ Play music from search queries
  - ⏸️ Pause/Resume playback
  - ⏭️ Skip to next track
  - ⏹️ Stop playback and disconnect
- **Interactive Controls**: Discord button-based UI for intuitive music control
- **Multiple Server Support**: Independently manage music for multiple Discord servers simultaneously

### AI Features
- **AI Chatbot**: Powered by Google Gemini API for intelligent responses
- **Long Response Handling**: Automatically converts lengthy responses to text files

### Additional Features
- **Keep-Alive System**: Flask-based health check endpoint to maintain bot connectivity
- **Voice Channel Detection**: Automatic validation that users are in voice channels
- **Real-time Status Updates**: Live now-playing message updates
- **Graceful Error Handling**: Comprehensive error management for stream issues

## 📋 Prerequisites

Before running this bot, ensure you have the following:

### Required Software
- **Python** 3.8 or higher (see `.python-version` for exact version)
- **FFmpeg** 7.0.2 (included in `Bin/` directory) or install separately
- **Git** (for cloning the repository)

### Required Accounts & API Keys
- **Discord Bot Token**: Create a bot application on Discord Developer Portal
- **Google Gemini API Key**: Get API key from Google AI Studio

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Dreem-R/Discord-Music-Bot.git
cd Discord-Music-Bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg (if not using bundled version)
**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://www.ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DISCORD_TOKEN=your_discord_bot_token_here
Gemini_Key=your_google_gemini_api_key_here
```

**How to obtain these tokens:**
- **DISCORD_TOKEN**: 
  1. Go to Discord Developer Portal
  2. Create a new application
  3. Go to "Bot" section and create a bot
  4. Copy the token under USERNAME

- **Gemini_Key**:
  1. Visit Google AI Studio
  2. Click "Get API Key"
  3. Copy your API key

### 5. Configure Bot Permissions

On Discord Developer Portal, ensure your bot has these permissions:

**Scopes:**
- `bot`
- `applications.commands`

**Permissions:**
- Send Messages
- Read Message History
- Connect (Voice)
- Speak (Voice)
- Use Slash Commands

## 🎮 Usage

### Starting the Bot

```bash
python MyBot.py
```

When the bot is running, you'll see:
```
YourBotName#0000 is ready
```

### Available Commands

All commands use Discord's slash command system (`/command`).

#### Music Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/mujik` | Play a song from YouTube | `/mujik song_query:Song Name or URL` |
| `/pause` | Pause current playback | `/pause` |
| `/resume` | Resume paused music | `/resume` |
| `/skip` | Skip to next track | `/skip` |
| `/stop` | Stop music and disconnect | `/stop` |

#### Other Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/search` | Ask the AI chatbot | `/search query:Your Question` |
| `/greet` | Get a friendly greeting | `/greet` |

### Interactive Controls

When music is playing, use the buttons that appear:
- **Pause** - Pause the current track
- **Resume** - Resume playing
- **Skip** - Skip to next track
- **Stop** - Stop all playback and leave voice channel

## 📁 Project Structure

```
Discord-Music-Bot/
├── MyBot.py              # Main bot application
├── KeepAlive.py          # Flask health check server
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .python-version       # Python version specification
├── Bin/                  # FFmpeg binary (if bundled)
└── README.md             # This file
```

### File Descriptions

- **MyBot.py**: Core bot logic handling Discord commands, music playback, queue management, and AI integration
- **KeepAlive.py**: Flask server running on port 8080 to keep the bot alive during long deployments
- **requirements.txt**: All Python package dependencies with pinned versions

## 🔧 Configuration

### Music Quality Settings

Edit the `YDL_OPTIONS` in `MyBot.py` (lines 159-165) to customize:

```python
YDL_OPTIONS = {
    'format': 'bestaudio/best',  # Audio quality preference
    'noplaylist': True,           # Prevent playlist downloads
    'quiet': False,               # Logging verbosity
    'no_warnings': False,         # Warning display
    'default_search': 'ytsearch', # Default search engine
}
```

### FFmpeg Settings

Modify `FFMPEG_OPTIONS` (lines 213-216) to adjust audio streaming:

```python
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10',
    'options': '-vn -bufsize 64k'  # Adjust buffer for stability
}
```

## 📚 Dependencies

### Core Dependencies
- **discord.py** (2.5.2): Discord API wrapper
- **yt-dlp** (2025.6.9): YouTube video downloader and extractor
- **python-dotenv** (1.1.0): Environment variable management
- **google-generativeai**: Google's Generative AI API client

### Additional Dependencies
- **Flask** (3.1.1): Web framework for keep-alive server
- **PyNaCl** (1.5.0): Voice encryption support
- **aiohttp**: Async HTTP client

See `requirements.txt` for the complete list with exact versions.

## 🚀 Deployment

### Hosting Considerations

This bot requires continuous runtime. Consider these deployment options:

#### Local Machine
- Simple setup for testing
- Requires your computer to stay on 24/7

#### Cloud Platforms
- **Replit**: Free tier available with keep-alive functionality
- **Railway.app**: Affordable with 500 free hours/month
- **Heroku**: Requires paid dyno (deprecated free tier)
- **VPS**: Full control on providers like DigitalOcean, AWS, or Linode

## 🐛 Troubleshooting

### Bot Not Responding
- Verify `DISCORD_TOKEN` is correct
- Ensure bot has proper Discord permissions
- Check that your bot is invited to the server
- Restart the bot application

### No Audio Streaming
- Verify FFmpeg is properly installed: `ffmpeg -version`
- Check FFmpeg path in `MyBot.py` (line 26)
- Ensure you're in a voice channel before using `/mujik`
- Check internet connection and YouTube availability

### "No Songs Found"
- Verify the song query is valid
- Check YouTube is accessible in your region
- Try searching by artist and song name separately

### Gemini API Issues
- Verify `Gemini_Key` is valid and not expired
- Check API quota isn't exceeded
- Ensure API key has proper permissions

### Bot Keeps Disconnecting
- Increase FFmpeg buffer: modify `FFMPEG_OPTIONS`
- Check internet stability
- Verify sufficient server resources

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Your Discord bot token | `YOUR_TOKEN_HERE` |
| `Gemini_Key` | Google Gemini API key | `YOUR_API_KEY_HERE` |

## 🔐 Security Notes

- **Never share your `.env` file** or commit it to version control
- Keep `.env` in `.gitignore` (already configured)
- Rotate API keys regularly
- Use strong, unique tokens
- Don't share bot token in public repositories

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💬 Support & Feedback

If you encounter issues or have suggestions:
- Open an Issue on GitHub
- Include detailed error messages and reproduction steps

## 🎯 Future Enhancements

Potential features for future development:
- [ ] Playlist support
- [ ] Music recommendation system
- [ ] Custom audio filters/effects
- [ ] Lyrics display integration
- [ ] Play history tracking
- [ ] User-specific playlists
- [ ] Volume control
- [ ] Shuffle and repeat modes
- [ ] Admin moderation commands

## 👨‍💻 Author

**Dreem-R**
- GitHub: [@Dreem-R](https://github.com/Dreem-R)

## 🙏 Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing
- [Google Generative AI](https://ai.google.dev/) - AI capabilities

---

**Last Updated**: 2026-03-27 10:03:44

**Disclaimer**: This bot streams content from YouTube. Ensure you comply with YouTube's Terms of Service and applicable copyright laws in your jurisdiction.