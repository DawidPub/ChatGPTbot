"""
Quick import test to verify modular architecture works
"""
print("Testing modular imports...")

try:
    from chatgpt_bot_core import ChatGPTBot
    print("✅ SUCCESS: chatgpt_bot_core imported successfully")
except ImportError as e:
    print(f"❌ ERROR: {e}")

try:
    from chatgpt_gui import ChatGPTGUI
    print("✅ SUCCESS: chatgpt_gui imported successfully")
except ImportError as e:
    print(f"❌ ERROR: {e}")

print("\nModular architecture test completed!")
input("Press Enter to exit...")
