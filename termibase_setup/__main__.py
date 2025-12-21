#!/usr/bin/env python3
"""
TermiBase Windows PATH Setup Helper
Run this after installing termibase to add it to your PATH automatically.
"""

import os
import sys
import site
from pathlib import Path

def find_scripts_dir():
    """Find where pip installed the termibase.exe script."""
    # Method 1: Use site.getusersitepackages()
    try:
        user_site = site.getusersitepackages()
        scripts_dir = Path(user_site).parent / "Scripts"
        if (scripts_dir / "termibase.exe").exists():
            return scripts_dir
    except Exception:
        pass
    
    # Method 2: Check common Windows locations
    user_profile = Path.home()
    python_versions = ["Python310", "Python311", "Python312", "Python313"]
    
    for version in python_versions:
        paths = [
            user_profile / "AppData" / "Roaming" / "Python" / version / "Scripts",
            user_profile / "AppData" / "Local" / "Programs" / "Python" / version / "Scripts",
        ]
        for path in paths:
            if (path / "termibase.exe").exists():
                return path
    
    return None

def add_to_path(scripts_dir):
    """Add scripts directory to user PATH."""
    scripts_path = str(scripts_dir)
    
    # Get current user PATH
    current_path = os.environ.get("PATH", "")
    
    # Check if already in PATH
    if scripts_path in current_path:
        print(f"✓ Scripts directory is already in PATH!")
        return True
    
    # Add to PATH
    try:
        import winreg
        
        # Open user environment variables
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Environment",
            0,
            winreg.KEY_ALL_ACCESS
        )
        
        # Get current PATH
        try:
            path_value, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            path_value = ""
        
        # Add new path if not already there
        if scripts_path not in path_value:
            new_path = f"{path_value};{scripts_path}" if path_value else scripts_path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            
            # Broadcast environment change
            import ctypes
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x001A, 0, "Environment")
            
            print(f"✓ Added {scripts_dir} to PATH successfully!")
            print("\n⚠️  Please restart your terminal for changes to take effect.")
            print("\n🎉 After restarting, you can use: termibase")
            return True
        else:
            print("✓ Already in PATH!")
            return True
            
    except ImportError:
        print("❌ Could not modify PATH automatically (winreg not available)")
        print(f"\nPlease add this directory to PATH manually:")
        print(f"   {scripts_dir}")
        return False
    except Exception as e:
        print(f"❌ Error adding to PATH: {e}")
        print(f"\nPlease add this directory to PATH manually:")
        print(f"   {scripts_dir}")
        return False

def main():
    print("🚀 TermiBase Windows PATH Setup")
    print()
    
    # Find scripts directory
    scripts_dir = find_scripts_dir()
    
    if not scripts_dir:
        print("❌ Could not find termibase.exe")
        print("\nMake sure termibase is installed:")
        print("   pip install termibase")
        print("\nYou can still use: python -m termibase")
        return 1
    
    print(f"Found TermiBase at: {scripts_dir}")
    print()
    
    # Ask user
    response = input("Add to PATH? (Y/n): ").strip().lower()
    if response == 'n':
        print("\n✓ Setup skipped.")
        print("You can use: python -m termibase")
        return 0
    
    # Add to PATH
    if add_to_path(scripts_dir):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())

