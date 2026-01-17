"""
Setup and Installation Script
Helps users set up the Discord Windows Control System
"""

import os
import sys


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_env_file():
    """Check if .env file exists."""
    if os.path.exists('.env'):
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("   Please copy .env.example to .env and fill in your credentials:")
        print("   cp .env.example .env")
        return False


def install_dependencies():
    """Guide user through dependency installation."""
    print("\n📦 To install dependencies, run:")
    print("   pip install -r requirements.txt")
    print("\nOr if you're using a virtual environment:")
    print("   python -m venv venv")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("   source venv/bin/activate")
    print("   pip install -r requirements.txt")


def show_next_steps():
    """Show next steps for user."""
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print()
    print("1. Install dependencies (see above)")
    print()
    print("2. Set up Discord Bot:")
    print("   - Go to https://discord.com/developers/applications")
    print("   - Create a new application")
    print("   - Add a bot and copy the token")
    print("   - Enable 'Message Content Intent' in Bot settings")
    print("   - Invite the bot to your server")
    print()
    print("3. Configure .env file:")
    print("   - Copy .env.example to .env")
    print("   - Add your DISCORD_TOKEN")
    print("   - Add your DISCORD_GUILD_ID (server ID)")
    print()
    print("4. Run the application:")
    print("   python main.py")
    print()
    print("5. Access the web interface:")
    print("   http://localhost:5000")
    print()
    print("=" * 60)


def main():
    """Run setup checks."""
    print("=" * 60)
    print("Discord Windows Control System - Setup")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check for .env file
    check_env_file()
    
    # Show installation instructions
    install_dependencies()
    
    # Show next steps
    show_next_steps()
    
    return 0


if __name__ == "__main__":
    exit(main())
