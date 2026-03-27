# Discord Music Bot

## Features
- Play music from various sources (YouTube, SoundCloud, etc.)
- Queue system for multiple songs
- Song search functionality
- Customizable play/pause/skip commands
- User-friendly interface

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Dreem-R/Discord-Music-Bot.git
   cd Discord-Music-Bot
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

## Usage Guide
- Invite the bot to your Discord server using the OAuth2 URL generated in the Discord developer portal.
- Use the command `!play <song name>` to start playing music.
- Manage the queue with `!skip`, `!pause`, and `!resume` commands.

## Dependencies
- discord.js
- @discordjs/voice
- dotenv
- axios

## Troubleshooting
- If the bot is not responding, ensure it is running and check the console for any error messages.
- Verify that all required dependencies are installed and up to date.

## Deployment
- Set up a hosting solution (e.g., Heroku, DigitalOcean).
- Use the provided environment variables for configuration.
- Deploy your bot using the hosting provider's guidelines.