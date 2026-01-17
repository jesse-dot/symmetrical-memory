"""
Main Application Entry Point
Runs both the Discord bot and web server concurrently.
"""

import threading
import os
from dotenv import load_dotenv
from discord_bot import run_bot
from web_server import run_server

# Load environment variables
load_dotenv()


def main():
    """Start both the Discord bot and web server."""
    print("=" * 60)
    print("Windows Device Control System")
    print("=" * 60)
    print()
    
    # Check for required environment variables
    if not os.getenv('DISCORD_TOKEN'):
        print("⚠️  Warning: DISCORD_TOKEN not found!")
        print("Please create a .env file based on .env.example")
        print()
    
    # Start web server in a separate thread
    web_thread = threading.Thread(target=run_server, daemon=True)
    web_thread.start()
    print("✅ Web server started")
    
    # Give the web server a moment to start
    import time
    time.sleep(2)
    
    print("✅ Starting Discord bot...")
    print()
    
    # Run Discord bot in main thread
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
