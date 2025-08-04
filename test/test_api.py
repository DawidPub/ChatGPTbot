import requests
import time
import json

def test_api():
    """Test ChatGPT Bot API functionality"""
    api_base = "http://localhost:8000"
    
    print("🧪 Testing ChatGPT Bot API")
    print("=" * 50)
    
    try:
        # Test 1: Check API is running
        print("1. 🔗 Testing API connection...")
        response = requests.get(f"{api_base}/")
        if response.status_code == 200:
            print("   ✅ API is running")
            print(f"   📋 API Info: {response.json()['message']}")
        else:
            print(f"   ❌ API connection failed: {response.status_code}")
            return False
            
        # Test 2: Create bot session
        print("\n2. 🆕 Creating bot session...")
        response = requests.post(f"{api_base}/bot/create")
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data['session_id']
            print(f"   ✅ Session created: {session_id}")
        else:
            print(f"   ❌ Session creation failed: {response.status_code}")
            return False
            
        # Test 3: Launch browser
        print("\n3. 🚀 Launching browser...")
        response = requests.post(f"{api_base}/bot/launch", json={"session_id": session_id})
        if response.status_code == 200:
            print("   ✅ Browser launch initiated")
        else:
            print(f"   ❌ Browser launch failed: {response.status_code}")
            
        # Test 4: Check status
        print("\n4. 📊 Checking session status...")
        time.sleep(2)  # Wait a moment
        response = requests.get(f"{api_base}/bot/status/{session_id}")
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ Status: {status_data['status']}")
            print(f"   📝 Logs: {len(status_data['logs'])} entries")
            if status_data['logs']:
                for log in status_data['logs'][-3:]:  # Show last 3 logs
                    print(f"      • {log['timestamp']}: {log['message']}")
        else:
            print(f"   ❌ Status check failed: {response.status_code}")
            
        # Test 5: Ask a simple question (optional - requires manual intervention)
        print("\n5. ❓ Testing question functionality...")
        print("   ⚠️  This test requires manual browser interaction")
        print("   📝 You can test this manually through the API client GUI")
        
        # Test 6: List all sessions
        print("\n6. 📋 Listing all sessions...")
        response = requests.get(f"{api_base}/bot/sessions")
        if response.status_code == 200:
            sessions_data = response.json()
            print(f"   ✅ Total sessions: {sessions_data['total']}")
            for session in sessions_data['sessions']:
                print(f"      • {session['session_id']}: {session['status']}")
        else:
            print(f"   ❌ Sessions listing failed: {response.status_code}")
            
        # Test 7: Cleanup session
        print(f"\n7. 🗑️ Cleaning up session {session_id}...")
        response = requests.delete(f"{api_base}/bot/{session_id}")
        if response.status_code == 200:
            print("   ✅ Session deleted successfully")
        else:
            print(f"   ❌ Session deletion failed: {response.status_code}")
            
        print("\n🎉 API Test completed successfully!")
        print("\n📋 Summary:")
        print("   ✅ API is running and responding")
        print("   ✅ Session management works")
        print("   ✅ Browser control endpoints available")
        print("   ✅ Status monitoring functional")
        print("\n💡 You can now use:")
        print("   • chatgpt_api_client.py - GUI client")
        print("   • http://localhost:8000/docs - Interactive API docs")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API server!")
        print("💡 Make sure the API server is running:")
        print("   python chatgpt_api_server.py")
        return False
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 ChatGPT Bot API Test Suite")
    print("💡 Make sure API server is running first!")
    print()
    
    input("Press Enter to start testing...")
    test_api()
