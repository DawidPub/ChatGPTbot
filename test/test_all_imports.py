"""
Test script to verify all modules can be imported correctly
"""
import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")
print()

# Test standard library imports
try:
    import json
    print("✅ json import: OK")
except ImportError as e:
    print(f"❌ json import failed: {e}")

try:
    import pickle
    print("✅ pickle import: OK")
except ImportError as e:
    print(f"❌ pickle import failed: {e}")

try:
    import os
    print("✅ os import: OK")
except ImportError as e:
    print(f"❌ os import failed: {e}")

try:
    import time
    print("✅ time import: OK")
except ImportError as e:
    print(f"❌ time import failed: {e}")

# Test third-party imports
try:
    import selenium
    print(f"✅ selenium import: OK (version {selenium.__version__})")
except ImportError as e:
    print(f"❌ selenium import failed: {e}")

try:
    import webdriver_manager
    print("✅ webdriver_manager import: OK")
except ImportError as e:
    print(f"❌ webdriver_manager import failed: {e}")

try:
    import tkinter
    print("✅ tkinter import: OK")
except ImportError as e:
    print(f"❌ tkinter import failed: {e}")

# Test local modules
try:
    import chatgpt_gui
    print("✅ chatgpt_gui import: OK")
except ImportError as e:
    print(f"❌ chatgpt_gui import failed: {e}")

try:
    import chatgpt_bot_core
    print("✅ chatgpt_bot_core import: OK")
except ImportError as e:
    print(f"❌ chatgpt_bot_core import failed: {e}")

print("\nAll import tests completed!")
input("Press Enter to exit...")
