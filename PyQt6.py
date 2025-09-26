"""
pyqt6.py – Utility to check and manage PyQt6 installation for Sparkwave-Insights
"""

import subprocess
import sys

# Minimum required PyQt6 version
MIN_VERSION = (6, 5, 0)

def check_pyqt6():
    """Check if PyQt6 is installed and meets the minimum version."""
    try:
        import PyQt6.QtCore # pyright: ignore[reportMissingImports]
        version_str = PyQt6.QtCore.PYQT_VERSION_STR
        version_tuple = tuple(int(x) for x in version_str.split('.'))
        if version_tuple >= MIN_VERSION:
            print(f"✅ PyQt6 is installed (version {version_str})")
            return True
        else:
            print(
                f"⚠️ PyQt6 version {version_str} detected. "
                f"Minimum required is {'.'.join(map(str, MIN_VERSION))}"
            )
            return False
    except ImportError:
        print("❌ PyQt6 is not installed")
        return False


def install_pyqt6():
    """Prompt user to install or upgrade PyQt6."""
    confirm = input("Do you want to install or upgrade PyQt6 now? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            print("📦 Installing/Upgrading PyQt6...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "PyQt6"])
            print("✅ PyQt6 installation/upgrade complete")
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
    else:
        print("ℹ️ Skipping installation.")


if __name__ == "__main__":
    if not check_pyqt6():
        install_pyqt6()
