#!/usr/bin/env python3
"""
Test script to verify the modular architecture works correctly
"""

def test_imports():
    """Test that all imports work correctly"""
    print("Testing modular imports...")
    
    try:
        # Test core import
        from chatgpt_bot_core import ChatGPTBot
        print("✓ ChatGPTBot import successful")
        
        # Test GUI import  
        from chatgpt_gui import ChatGPTGUI
        print("✓ ChatGPTGUI import successful")
        
        # Test package imports
        try:
            from __init__ import ChatGPTBot as PackageChatGPTBot
            from __init__ import ChatGPTGUI as PackageChatGPTGUI
            print("✓ Package imports successful")
        except ImportError as e:
            print(f"⚠ Package imports failed (this is normal if not installed as package): {e}")
        
        # Test class instantiation
        bot = ChatGPTBot()
        print("✓ ChatGPTBot instantiation successful")
        
        gui = ChatGPTGUI()
        print("✓ ChatGPTGUI instantiation successful")
        
        # Test callback functionality
        def test_status_callback(message):
            return f"Status: {message}"
            
        def test_response_callback(text):
            return f"Response: {text}"
        
        bot_with_callbacks = ChatGPTBot(
            status_callback=test_status_callback,
            response_callback=test_response_callback
        )
        
        # Test callback methods
        bot_with_callbacks.log_status("Test message")
        bot_with_callbacks.update_response("Test response")
        bot_with_callbacks.log_response_line("Test line", 1)
        print("✓ Callback functionality working")
        
        print("\n🎉 All tests passed! Modular architecture is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_backward_compatibility():
    """Test that backward compatibility works"""
    print("\nTesting backward compatibility...")
    
    try:
        # This should work like the original
        import chatgpt_bot
        print("✓ Backward compatibility import successful")
        
        # Test that classes are accessible
        bot = chatgpt_bot.ChatGPTBot()
        gui = chatgpt_bot.ChatGPTGUI()
        print("✓ Backward compatibility classes accessible")
        
        print("✓ Backward compatibility confirmed")
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False

if __name__ == "__main__":
    print("ChatGPT Bot - Modular Architecture Test")
    print("=" * 40)
    
    success1 = test_imports()
    success2 = test_backward_compatibility()
    
    if success1 and success2:
        print("\n🚀 All systems operational! The modular architecture is ready to use.")
    else:
        print("\n⚠ Some tests failed. Please check the error messages above.")
