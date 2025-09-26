import subprocess
import sys

# Minimum required PyQt6 version (example)
MIN_VERSION = (6, 5, 0)

def check_pyqt6():
    try:
        import PyQt6.QtCore
        version_str = PyQt6.QtCore.PYQT_VERSION_STR
        version_tuple = tuple(int(x) for x in version_str.split('.'))
        if version_tuple >= MIN_VERSION:
            print(f"✅ PyQt6 is installed, version {version_str}")
            return True
        else:
            print(f"⚠️ PyQt6 version is {version_str}, minimum required is {'.'.join(map(str, MIN_VERSION))}")
            return False
    except ImportError:
        print("❌ PyQt6 is not installed")
        return False

def install_pyqt6():
    confirm = input("Do you want to install or upgrade PyQt6 now? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            print("Installing/Upgrading PyQt6...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "PyQt6"])
            print("✅ PyQt6 installation complete!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            sys.exit(1)
    else:
        print("PyQt6 is required to run this program. Exiting...")
        sys.exit(1)

if not check_pyqt6():
    install_pyqt6()

# Safe to import now
from PyQt6.QtCore import PYQT_VERSION_STR, QT_VERSION_STR
print(f"Running PyQt6 {PYQT_VERSION_STR} with Qt {QT_VERSION_STR}")


import subprocess
import sys

# Minimum required version (optional)
MIN_VERSION = (0, 6, 21)  # example minimum version of python-pptx

def check_pptx():
    try:
        import pptx
        version_str = pptx.__version__
        version_tuple = tuple(int(x) for x in version_str.split('.'))
        if version_tuple >= MIN_VERSION:
            print(f"✅ python-pptx is installed, version {version_str}")
            return True
        else:
            print(f"⚠️ python-pptx version is {version_str}, minimum required is {'.'.join(map(str, MIN_VERSION))}")
            return False
    except ImportError:
        print("❌ python-pptx is not installed")
        return False

def install_pptx():
    confirm = input("Do you want to install or upgrade python-pptx now? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            print("Installing/Upgrading python-pptx...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "python-pptx"])
            print("✅ python-pptx installation complete!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            sys.exit(1)
    else:
        print("python-pptx is required to run this program. Exiting...")
        sys.exit(1)

if not check_pptx():
    install_pptx()

# After this, you can safely import pptx
from pptx import Presentation
print("You can now use python-pptx!")
