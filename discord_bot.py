"""
Discord Windows Control Bot
A Discord bot that allows remote control of a Windows device via slash commands
and provides real-time screen streaming through a web interface.
"""

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import io
import os
from dotenv import load_dotenv
import pyautogui
import mss
from PIL import Image

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

# PyAutoGUI safety configuration
# FAILSAFE is enabled by default - moving mouse to corner stops automation
# This is a safety feature to prevent runaway automation
pyautogui.FAILSAFE = True  # Keep enabled for safety
pyautogui.PAUSE = 0.1  # Add a small pause between PyAutoGUI calls

# Initialize bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Sync slash commands
    try:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f'Synced commands to guild {GUILD_ID}')
        else:
            await bot.tree.sync()
            print('Synced commands globally')
    except Exception as e:
        print(f'Error syncing commands: {e}')


@bot.tree.command(name="screenshot", description="Take a screenshot of the Windows device")
async def screenshot(interaction: discord.Interaction):
    """Take a screenshot and send it to Discord."""
    await interaction.response.defer(ephemeral=False)
    
    try:
        # Capture screenshot using mss (faster than pyautogui)
        with mss.mss() as sct:
            # Validate that monitors are available
            if len(sct.monitors) < 2:
                await interaction.followup.send("❌ No monitors detected!")
                return
            
            monitor = sct.monitors[1]  # Primary monitor
            screenshot_data = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot_data.size, screenshot_data.bgra, 'raw', 'BGRX')
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Send to Discord
        file = discord.File(img_bytes, filename='screenshot.png')
        await interaction.followup.send(
            content="📸 Screenshot captured!",
            file=file
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Error capturing screenshot: {str(e)}")


@bot.tree.command(name="click", description="Click the mouse at specified coordinates")
@app_commands.describe(
    x="X coordinate",
    y="Y coordinate",
    button="Mouse button to click (left, right, middle)"
)
async def click(interaction: discord.Interaction, x: int, y: int, button: str = "left"):
    """Simulate a mouse click at the specified coordinates."""
    await interaction.response.defer(ephemeral=False)
    
    try:
        if button not in ["left", "right", "middle"]:
            await interaction.followup.send("❌ Invalid button. Use 'left', 'right', or 'middle'.")
            return
        
        pyautogui.click(x, y, button=button)
        await interaction.followup.send(f"✅ Clicked {button} button at ({x}, {y})")
    except Exception as e:
        await interaction.followup.send(f"❌ Error clicking: {str(e)}")


@bot.tree.command(name="type", description="Type text on the Windows device")
@app_commands.describe(text="Text to type")
async def type_text(interaction: discord.Interaction, text: str):
    """Type the specified text."""
    await interaction.response.defer(ephemeral=False)
    
    try:
        pyautogui.write(text, interval=0.05)
        await interaction.followup.send(f"⌨️ Typed: {text}")
    except Exception as e:
        await interaction.followup.send(f"❌ Error typing: {str(e)}")


@bot.tree.command(name="press", description="Press a keyboard key")
@app_commands.describe(key="Key to press (e.g., 'enter', 'tab', 'esc', 'space')")
async def press(interaction: discord.Interaction, key: str):
    """Press a keyboard key."""
    await interaction.response.defer(ephemeral=False)
    
    try:
        pyautogui.press(key.lower())
        await interaction.followup.send(f"⌨️ Pressed: {key}")
    except Exception as e:
        await interaction.followup.send(f"❌ Error pressing key: {str(e)}")


@bot.tree.command(name="move", description="Move the mouse to specified coordinates")
@app_commands.describe(
    x="X coordinate",
    y="Y coordinate",
    duration="Duration of movement in seconds"
)
async def move(interaction: discord.Interaction, x: int, y: int, duration: float = 0.5):
    """Move the mouse to the specified coordinates."""
    await interaction.response.defer(ephemeral=False)
    
    try:
        pyautogui.moveTo(x, y, duration=duration)
        await interaction.followup.send(f"🖱️ Moved mouse to ({x}, {y})")
    except Exception as e:
        await interaction.followup.send(f"❌ Error moving mouse: {str(e)}")


@bot.tree.command(name="screeninfo", description="Get screen resolution information")
async def screeninfo(interaction: discord.Interaction):
    """Get screen resolution information."""
    await interaction.response.defer(ephemeral=False)
    
    try:
        screen_size = pyautogui.size()
        with mss.mss() as sct:
            monitors_info = []
            for i, monitor in enumerate(sct.monitors[1:], 1):
                monitors_info.append(
                    f"Monitor {i}: {monitor['width']}x{monitor['height']} "
                    f"at ({monitor['left']}, {monitor['top']})"
                )
        
        info_message = f"🖥️ **Screen Information**\n"
        info_message += f"Primary Screen: {screen_size[0]}x{screen_size[1]}\n"
        info_message += "\n".join(monitors_info)
        
        await interaction.followup.send(info_message)
    except Exception as e:
        await interaction.followup.send(f"❌ Error getting screen info: {str(e)}")


@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    """Display help information."""
    help_text = """
🎮 **Windows Device Control Commands**

**/screenshot** - Take a screenshot of the device
**/click <x> <y> [button]** - Click at coordinates (button: left/right/middle)
**/type <text>** - Type text on the device
**/press <key>** - Press a keyboard key (enter, tab, esc, etc.)
**/move <x> <y> [duration]** - Move mouse to coordinates
**/screeninfo** - Get screen resolution information
**/help** - Show this help message

🌐 **Web Interface**
Access the real-time screen viewer at: http://localhost:5000
    """
    await interaction.response.send_message(help_text, ephemeral=True)


def run_bot():
    """Run the Discord bot."""
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your Discord bot token.")
        return
    
    bot.run(TOKEN)


if __name__ == "__main__":
    run_bot()
