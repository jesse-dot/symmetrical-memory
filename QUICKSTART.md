# Quick Start Guide

## 5-Minute Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Discord Bot

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" section and click "Add Bot"
4. Copy your bot token
5. Enable "Message Content Intent" under Privileged Gateway Intents
6. Go to OAuth2 → URL Generator:
   - Scopes: `bot`, `applications.commands`
   - Permissions: `Send Messages`, `Attach Files`
7. Copy the URL and invite bot to your server

### 3. Get Your Guild (Server) ID

1. Enable Developer Mode in Discord:
   - User Settings → App Settings → Advanced → Developer Mode
2. Right-click your server icon and click "Copy ID"

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add:
```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id_here
```

### 5. Run the Application

```bash
python main.py
```

### 6. Use the System

**Discord Commands:**
- Open Discord and type `/` to see available commands
- Try `/screenshot` to capture the screen
- Use `/help` for all commands

**Web Interface:**
- Open browser to `http://localhost:5000`
- View real-time screen streaming

## Example Commands

```
/screenshot                          # Take a screenshot
/click 500 300                       # Click at coordinates (500, 300)
/click 500 300 right                # Right-click at coordinates
/type Hello World                    # Type text
/press enter                         # Press Enter key
/move 800 600                        # Move mouse to (800, 600)
/screeninfo                          # Get screen information
```

## Troubleshooting

**Commands not showing up?**
- Wait a few minutes after inviting the bot
- Restart the bot
- Check bot permissions in server settings

**Can't access web server?**
- Check firewall settings
- Make sure port 5000 is not in use
- Try `http://127.0.0.1:5000` instead

**Permission errors?**
- Run as administrator on Windows
- Some applications block automation

## Security Note

⚠️ This gives full control of your computer! Only use in trusted Discord servers.
