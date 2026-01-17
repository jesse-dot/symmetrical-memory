# Windows Device Control via Discord 🎮

A powerful Discord bot that allows you to remotely control a Windows device using slash commands and view its screen in real-time through a web interface.

## Features

### Discord Slash Commands 🤖
- `/screenshot` - Capture and receive a screenshot of the Windows device
- `/click <x> <y> [button]` - Click the mouse at specified coordinates
- `/type <text>` - Type text on the device keyboard
- `/press <key>` - Press specific keyboard keys (enter, tab, esc, etc.)
- `/move <x> <y> [duration]` - Move the mouse cursor to coordinates
- `/screeninfo` - Get screen resolution and monitor information
- `/help` - Display all available commands

### Real-Time Web Viewer 🌐
- Live screen streaming at configurable FPS
- Clean, modern web interface
- Accessible from any browser on the network
- Low-latency MJPEG streaming

## Prerequisites

- Python 3.8 or higher
- Windows operating system (for the controlled device)
- Discord Bot Token and Server (Guild) ID

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jesse-dot/symmetrical-memory.git
   cd symmetrical-memory
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root (use `.env.example` as template):
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_GUILD_ID=your_guild_id_here
   WEB_SERVER_HOST=0.0.0.0
   WEB_SERVER_PORT=5000
   ```

## Getting Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" section
4. Click "Add Bot"
5. Under "TOKEN", click "Copy" to get your bot token
6. Enable the following Privileged Gateway Intents:
   - Message Content Intent
7. Go to OAuth2 → URL Generator
8. Select scopes: `bot`, `applications.commands`
9. Select bot permissions: `Send Messages`, `Attach Files`
10. Copy the generated URL and open it to invite the bot to your server

## Usage

### Running the Application

**Option 1: Run everything together (recommended)**
```bash
python main.py
```

**Option 2: Run components separately**

Terminal 1 - Discord Bot:
```bash
python discord_bot.py
```

Terminal 2 - Web Server:
```bash
python web_server.py
```

### Accessing the Web Interface

Once running, open your browser and navigate to:
```
http://localhost:5000
```

Or from another device on the same network:
```
http://<your-pc-ip-address>:5000
```

## Project Structure

```
symmetrical-memory/
├── main.py              # Main entry point (runs bot + web server)
├── discord_bot.py       # Discord bot with slash commands
├── web_server.py        # Flask web server for screen streaming
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your environment configuration (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Dependencies

- **discord.py** - Discord bot framework
- **flask** - Web server framework
- **pillow** - Image processing
- **mss** - Fast screenshot capture
- **pyautogui** - Mouse and keyboard control
- **python-dotenv** - Environment variable management

## Security Considerations

⚠️ **Important Security Notes:**

1. **Access Control**: This tool gives full control over your Windows device. Only use it in trusted Discord servers with trusted members.

2. **Token Security**: Never share your `.env` file or Discord bot token publicly.

3. **Network Security**: The web server is accessible to anyone on your network by default. Consider:
   - Using a firewall to restrict access
   - Running on localhost only (set `WEB_SERVER_HOST=127.0.0.1`)
   - Implementing authentication if needed

4. **Permissions**: Review Discord bot permissions carefully. Only grant what's necessary.

## Configuration

### Adjusting Stream Quality

Edit `web_server.py` to modify:
- `FPS` - Frames per second (default: 10)
- Image quality in `generate_frames()` function
- Resolution scaling (currently commented out)

### Discord Command Permissions

To restrict commands to specific roles, modify the command decorators in `discord_bot.py` using Discord's permission system.

## Troubleshooting

**Bot not responding to slash commands:**
- Ensure the bot has proper permissions in your Discord server
- Wait a few minutes after inviting the bot (commands may take time to sync)
- Try re-syncing commands by restarting the bot

**Web server not accessible:**
- Check firewall settings
- Verify the port is not in use by another application
- Ensure `WEB_SERVER_HOST` is set correctly in `.env`

**Screenshot/control not working:**
- Ensure you're running on Windows
- Check that pyautogui has necessary permissions
- Some fullscreen applications may block automation

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and personal use. Users are responsible for ensuring compliance with their organization's policies and applicable laws regarding remote access and control of computer systems.