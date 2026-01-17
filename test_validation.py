"""
Basic validation tests for the Discord Windows Control System
Tests import functionality and basic structure validation.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import discord_bot
        print("✓ discord_bot imported successfully")
    except Exception as e:
        print(f"✗ Failed to import discord_bot: {e}")
        return False
    
    try:
        import web_server
        print("✓ web_server imported successfully")
    except Exception as e:
        print(f"✗ Failed to import web_server: {e}")
        return False
    
    try:
        import main
        print("✓ main imported successfully")
    except Exception as e:
        print(f"✗ Failed to import main: {e}")
        return False
    
    return True


def test_dependencies():
    """Test that all required dependencies are available."""
    print("\nTesting dependencies...")
    
    # Map package names to their import names
    package_mapping = {
        'discord': 'discord',
        'flask': 'flask',
        'pillow': 'PIL',
        'mss': 'mss',
        'pyautogui': 'pyautogui',
        'python-dotenv': 'dotenv'
    }
    
    all_available = True
    for package_name, import_name in package_mapping.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name} ({import_name}) is available")
        except ImportError:
            print(f"✗ {package_name} ({import_name}) is NOT available")
            all_available = False
    
    return all_available


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        'discord_bot.py',
        'web_server.py',
        'main.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        '.gitignore'
    ]
    
    all_exist = True
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    for file in required_files:
        file_path = os.path.join(base_path, file)
        if os.path.exists(file_path):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} does NOT exist")
            all_exist = False
    
    return all_exist


def test_discord_bot_structure():
    """Test Discord bot has required commands."""
    print("\nTesting Discord bot structure...")
    
    try:
        import discord_bot
        
        # Check if bot instance exists
        if hasattr(discord_bot, 'bot'):
            print("✓ Bot instance exists")
        else:
            print("✗ Bot instance not found")
            return False
        
        # Check for command functions (they exist as functions before registration)
        commands = ['screenshot', 'click', 'type_text', 'press', 'move', 'screeninfo', 'help_command']
        for cmd in commands:
            if hasattr(discord_bot, cmd):
                print(f"✓ Command '{cmd}' defined")
            else:
                print(f"✗ Command '{cmd}' not found")
        
        return True
    except Exception as e:
        print(f"✗ Error testing Discord bot: {e}")
        return False


def test_web_server_structure():
    """Test web server has required routes."""
    print("\nTesting web server structure...")
    
    try:
        import web_server
        
        # Check if Flask app exists
        if hasattr(web_server, 'app'):
            print("✓ Flask app instance exists")
            
            # Check routes
            routes = [rule.rule for rule in web_server.app.url_map.iter_rules()]
            expected_routes = ['/', '/video_feed', '/health']
            
            for route in expected_routes:
                if route in routes:
                    print(f"✓ Route '{route}' exists")
                else:
                    print(f"✗ Route '{route}' not found")
        else:
            print("✗ Flask app instance not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error testing web server: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Discord Windows Control System - Validation Tests")
    print("=" * 60)
    print()
    
    results = {
        'File Structure': test_file_structure(),
        'Dependencies': test_dependencies(),
        'Imports': test_imports(),
        'Discord Bot Structure': test_discord_bot_structure(),
        'Web Server Structure': test_web_server_structure()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    exit(main())
